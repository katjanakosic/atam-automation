import json
from pathlib import Path
from typing import List, Optional

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
    return mapping


def run_base_pipeline(
    *,
    domain_dir: str | Path,
    out_root: str | Path = "outputs",
    prompt_path: str | Path = "prompts/base_scenario_mapping.md",
    ollama_host: str = "localhost:8000",
    ollama_model: str = "llama3.2:3b",
    max_retries: int = 2,
    reuse_existing_mappings: bool = True,
) -> Path:
    """

    :param domain_dir:
    :param out_root:
    :param prompt_path:
    :param ollama_host:
    :param ollama_model:
    :param max_retries:
    :param reuse_existing_mappings:
    :return:
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
    llm = create_typed_llm(model=ollama_model, host=ollama_host)

    # Phase 1: Scenario×Architecture mapping
    all_mappings: List[ScenarioArchitectureMapping] = []
    for architecture in architectures:
        for scenario in scenarios:
            out_file = mappings_dir / f"{architecture.id}_{scenario.id}.json"

            if reuse_existing_mappings and out_file.exists():
                loaded = ScenarioArchitectureMapping.model_validate(read_json(out_file))
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
                # Write an error file so expert evaluators can inspect failures
                write_json(out_file.with_suffix(".error.json"), {"error": str(last_error)})

    # Phase 2: Sensitivity identification
    sensitivities = compute_component_sensitivities(all_mappings)
    write_json(metrics_dir / "component_sensitivities.json", [sensitivity.model_dump() for sensitivity in sensitivities] )

    # Phase 3: Tradeoff detection
    tradeoffs = detect_component_tradeoffs(all_mappings)
    write_json(metrics_dir / "tradeoffs.json", [tradeoff.model_dump() for tradeoff in tradeoffs])

    # Phase 4: Summary
    summaries = build_architecture_summaries(sensitivities, tradeoffs, top_k=5)
    write_json(metrics_dir / "architecture_summaries.json", [summary.model_dump() for summary in summaries])

    # Run index
    write_json(run_dir / "run_index.json", {
        "domain": domain_dir.name,
        "inputs": {
            "scenarios": str(scenarios_path),
            "architecturesDir": str(architectures_path),
            "prompt": str(prompt_path),
        },
        "ollama": {
            "host": ollama_host,
            "model": ollama_model,
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
