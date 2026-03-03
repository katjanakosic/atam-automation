import json
from pathlib import Path
from typing import List, Optional, Set

from pydantic import TypeAdapter

from atam.datatypes import Scenario, Architecture, ScenarioArchitectureMapping
from atam.io_utils import read_json, make_run_dir, write_json
from atam.metrics import compute_component_sensitivities, detect_component_tradeoffs, build_architecture_summaries
from common.llm_access import create_prompt, create_typed_llm


def _load_scenarios(scenarios_path: Path) -> List[Scenario]:
    """
    Load and validate scenarios from JSON file.

    :param scenarios_path: Path to the JSON file containing scenarios
    :returns: List of validated Scenario objects
    """
    raw = read_json(scenarios_path)
    return TypeAdapter(List[Scenario]).validate_python(raw)


def _load_architectures(architectures_dir: str | Path) -> List[Architecture]:
    """
    Load and validate all architecture files from directory.

    :param architectures_dir: Path to directory containing architecture JSON files
    :return: List of validated Architecture objects, sorted by filename
    """
    architecture_dir = Path(architectures_dir)
    architecture_files = sorted(architecture_dir.glob("*.json"))
    out: List[Architecture] = []
    for f in architecture_files:
        out.append(Architecture.model_validate(read_json(f)))
    return out

ALLOWED_STRENGTH: Set[float] = {0.1, 0.3, 0.5, 0.7, 0.9}
ALLOWED_CONFIDENCE: Set[float] = {0.2, 0.4, 0.6, 0.8, 1.0}


def _nearest_allowed(x: float, allowed: Set[float]) -> float:
    """
    Snap a numeric value to the nearest value in an allowed discrete set

    :param x: value to snap
    :param allowed: allowed discrete set
    :return: minimum allowed value
    """

    return min(allowed, key=lambda a: abs(a - float(x)))


def _is_interaction_path(evidence_item: str) -> bool:
    return "->" in evidence_item


def _calibrate_effect(effect) -> None:
    """
    Enforce discrete scales and gate confidence by evidence.
    - strength & confidence snapped to allowed sets (eliminates false precision)
    - confidence is downgraded if evidence does not justify the level
    :param effect: effect to enforce
    """
    # snap to discrete sets (in case a model outputs 0.73, etc.)
    try:
        effect.strength = _nearest_allowed(effect.strength, ALLOWED_STRENGTH)
    except Exception:
        effect.strength = 0.5  # safe default

    try:
        effect.confidence = _nearest_allowed(effect.confidence, ALLOWED_CONFIDENCE)
    except Exception:
        effect.confidence = 0.4  # safe default

    evidence = getattr(effect, "evidence", None) or []
    ev_count = len(evidence)
    has_path = any(_is_interaction_path(e) for e in evidence)

    if ev_count == 0:
        effect.confidence = 0.2
        return

    # Rubric-based ceilings
    # 0.6 requires >=1 explicit fact
    # 0.8 requires >=2 facts OR 1 explicit interaction path
    # 1.0 requires >=2 facts AND a direct causal interaction path
    if effect.confidence >= 1.0:
        if not (ev_count >= 2 and has_path):
            effect.confidence = 0.8 if (ev_count >= 2 or has_path) else 0.6
        return

    if effect.confidence >= 0.8:
        if not (ev_count >= 2 or has_path):
            effect.confidence = 0.6
        return

    if effect.confidence >= 0.6:
        if ev_count < 1:
            effect.confidence = 0.4
        return


def _calibrate_mapping(mapping: ScenarioArchitectureMapping) -> ScenarioArchitectureMapping:
    """
    Post-processing validation and correction layer (applied after LLM generates a ScenarioArchitectureMapping)
    - prevents confidence inflation
    - ensures rubric adherence

    :param mapping: mapping to be calibrated
    :return: mapping with calibration applied
    """
    for component_impact in mapping.componentImpacts:
        for effect in component_impact.effects:
            _calibrate_effect(effect)
    return mapping



def _run_mapping(llm, prompt_path: str | Path, scenario: Scenario,
                 architecture: Architecture) -> ScenarioArchitectureMapping:
    scenario_json = json.dumps(scenario.model_dump(), indent=2)
    architecture_json = json.dumps(architecture.model_dump(), indent=2) # model_dump: generate a dictionary representation of the model, optionally specifying which fields to include or exclude

    prompt = create_prompt(file=str(prompt_path), scenario_json=scenario_json, architecture_json=architecture_json)

    message = llm.generate(ScenarioArchitectureMapping, prompt, debug=lambda x: x, use_example_for_formatting=True)

    mapping: ScenarioArchitectureMapping = message.response

    mapping.architectureId = architecture.id
    mapping.scenarioId = scenario.id
    mapping.qualityAttribute = scenario.qualityAttribute
    mapping = _calibrate_mapping(mapping)
    return mapping


def run_base_pipeline(
    *,
    domain_dir: str | Path,
    out_root: str | Path = "outputs",
    prompt_path: str | Path = "prompts/base_scenario_mapping.md",
    ollama_host: str = "localhost:8000",
    model: str = "anthropic/claude-haiku-4.5",
    max_retries: int = 2,
    reuse_existing_mappings: bool = True,
    provider: str = "ollama",
    openrouter_api_key: Optional[str] = None,
    openrouter_base_url: str = "https://openrouter.ai/api/v1",
) -> Path:
    """
    Execute the base ATAM automation pipeline for a given domain.

    The pipeline performs the following steps:
    0. Load scenarios and architecture descriptions from the specified domain
    1. Generate Scenario×Architecture mappings
    2. Compute component sensitivities
    3. Detect architectural trade-offs
    4. Generate summary of findings
    5. Produce a run index for traceability

    :param domain_dir: Path to domain directory
    :param out_root: Root directory under which a timestamped run folder will be created
    :param prompt_path: Path to the prompt template used for scenario–architecture mapping
    :param ollama_host: Base URL of the Ollama server (used only if provider="ollama")
    :param model: Model identifier used by the selected provider.
    :param max_retries: Maximum number of retries per scenario–architecture mapping if generation / validation fails
    :param reuse_existing_mappings: If True, existing mapping JSON files in the output directory are reused instead of regenerating them
    :param provider: LLM provider (either "ollama" or "openrouter")
    :param openrouter_api_key: OpenRouter API key (if None: value is read from environment variables)
    :param openrouter_base_url: OpenRouter base URL (if None: value is read from environment variables)
    :return: Path to the created run directory containing mappings, metrics, summaries and runs
    """

    # Phase 0: Load data
    domain_dir = Path(domain_dir)
    scenarios_path = domain_dir / "scenarios.json"
    architectures_path = domain_dir / "architectures"

    scenarios = _load_scenarios(scenarios_path)
    architectures = _load_architectures(architectures_path)

    run_dir = make_run_dir(out_root, domain_dir.name)
    mappings_dir = run_dir / "mappings"
    metrics_dir = run_dir / "metrics"
    summary_dir = run_dir / "summary"

    # LLM
    llm = create_typed_llm(
        model=model,
        host=ollama_host,
        provider=provider,
        openrouter_api_key=openrouter_api_key,
        openrouter_base_url=openrouter_base_url,
    )

    # Phase 1: Scenario×Architecture mapping
    all_mappings: List[ScenarioArchitectureMapping] = []
    for architecture in architectures:
        for scenario in scenarios:
            out_file = mappings_dir / f"{architecture.id}_{scenario.id}.json"

            if reuse_existing_mappings and out_file.exists():
                loaded = ScenarioArchitectureMapping.model_validate(read_json(out_file))
                loaded = _calibrate_mapping(loaded)  # keep metrics consistent
                all_mappings.append(loaded)
                continue

            last_error: Optional[Exception] = None
            for attempt in range(max_retries + 1):
                try:
                    mapping = _run_mapping(llm, prompt_path, scenario, architecture)
                    write_json(out_file, mapping.model_dump())
                    all_mappings.append(mapping)
                    last_error = None
                    break
                except Exception as e:
                    last_error = e

            if last_error is not None:
                # write an error file so expert evaluators can inspect failures
                write_json(out_file.with_suffix(".error.json"), {"error": str(last_error)})

    # Phase 2: Sensitivity identification
    sensitivities = compute_component_sensitivities(all_mappings)
    write_json(metrics_dir / "component_sensitivities.json", [sensitivity.model_dump() for sensitivity in sensitivities] )

    # Phase 3: Tradeoff detection
    tradeoffs = detect_component_tradeoffs(all_mappings)
    write_json(metrics_dir / "tradeoffs.json", [tradeoff.model_dump() for tradeoff in tradeoffs])

    # Phase 4: Summary
    summaries = build_architecture_summaries(sensitivities, tradeoffs, top_k=5)
    write_json(summary_dir / "architecture_summaries.json", [summary.model_dump() for summary in summaries])

    # Phase 5: Run index
    write_json(run_dir / "run_index.json", {
        "domain": domain_dir.name,
        "inputs": {
            "scenarios": str(scenarios_path),
            "architecturesDir": str(architectures_path),
            "prompt": str(prompt_path),
        },
        "llm": {
                "provider": provider,
                "ollama": {
                    "host": ollama_host,
                    "model": model,
                } if provider == "ollama" else None,
                "openrouter": {
                    "base_url": openrouter_base_url,
                    "model": model,
                } if provider == "openrouter" else None,
            },
        "outputs": {
            "mappingsDir": str(mappings_dir),
            "sensitivities": str(metrics_dir / "component_sensitivities.json"),
            "tradeoffs": str(metrics_dir / "tradeoffs.json"),
            "summaries": str(summary_dir / "architecture_summaries.json"),
        },
        "counts": {
            "scenarios": len(scenarios),
            "architectures": len(architectures),
            "mappingsExpected": len(scenarios) * len(architectures),
            "mappingsProduced": len([p for p in mappings_dir.glob("*.json")]),
        }
    })

    return run_dir
