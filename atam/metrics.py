from collections import defaultdict
from typing import List, Dict, Tuple

from atam.datatypes import ScenarioArchitectureMapping, ComponentSensitivity, Tradeoff, ArchitectureSummary


def compute_component_sensitivities(mappings: List[ScenarioArchitectureMapping]) -> List[ComponentSensitivity]:
    """
    Calculate sensitivity scores for each component-attribute pair across all architectures.

    Sensitivity measures how much a component affects a quality attribute.
    Calculation = average of (strength × confidence) across all scenarios that involve that component.
    Higher sensitivity => component has a stronger impact on that quality attribute.

    :param mappings: List of scenario-architecture mappings containing component impacts
    :return: List of ComponentSensitivity objects with calculated sensitivity scores
    """
    # group scores by (architecture_id, component, attribute)
    bucket: Dict[Tuple[str, str, str], List[float]] = defaultdict(list)

    for mapping in mappings:
        architecture_id = mapping.architecture_id
        attribute = mapping.qualityAttribute
        for impact in mapping.componentImpacts:
            for effect in impact.effects:
                # impact score = strength × confidence (ignoring positive/negative direction)
                score = float(effect.strength) * float(effect.confidence)
                bucket[(architecture_id, impact.component, attribute)].append(score)

    # average sensitivity for each (architecture, component, attribute) combination
    out: List[ComponentSensitivity] = []
    for (architecture_id, component, attribute), scores in bucket.items():
        sensitivity = sum(scores) / len(scores)
        out.append(
            ComponentSensitivity(
                architectureId=architecture_id,
                component=component,
                attribute=attribute,
                sensitivity=round(float(sensitivity), 4),
            )
        )
    return out


def detect_component_tradeoffs(mappings: List[ScenarioArchitectureMapping]) -> List[Tradeoff]:
    """
    Identify architectural tradeoffs where a component positively affects one quality attribute
    but negatively affects another.

    :param mappings: List of scenario-architecture mappings containing component impacts
    :return: List of Tradeoff objects
    """
    # track which effect signs (positive/negative) appear for each (architecture, component, attribute)
    signs = defaultdict(set)
    evidence = {}

    for mapping in mappings:
        architecture_id = mapping.architectureId
        attribute = mapping.qualityAttribute
        for impact in mapping.componentImpacts:
            for effect in impact.effects:
                signs[(architecture_id, impact.component, attribute)].add(effect.effectSign.value)
                key = (architecture_id, impact.component, attribute, effect.effectSign.value)
                evidence.setdefault(key, effect.explanation)

    # for each (architecture, component) tuple collect attributes by sign
    positive_attributes = defaultdict(set)  # (arch, comp) -> {attr}
    negative_attributes = defaultdict(set)

    for (architecture, component, attribute), sign in signs.items():
        if "positive" in sign:
            positive_attributes[(architecture, component)].add(attribute)
        if "negative" in sign:
            negative_attributes[(architecture, component)].add(attribute)

    tradeoffs: List[Tradeoff] = []
    for (architecture, component), pos_attributes in positive_attributes.items():
        neg_attributes = negative_attributes.get((architecture, component), set())
        if not neg_attributes:
            continue

        # create a tradeoff entry for each pair of conflicting attributes
        for a_pos in sorted(pos_attributes):
            for a_neg in sorted(neg_attributes):
                if a_pos == a_neg:
                    continue
                ev_pos = evidence.get((architecture, component, a_pos, "positive"), "")
                ev_neg = evidence.get((architecture, component, a_neg, "negative"), "")
                ev = f"+ {a_pos}: {ev_pos} | - {a_neg}: {ev_neg}".strip()

                tradeoffs.append(
                    Tradeoff(
                        architectureId=architecture,
                        component=component,
                        attributePositive=a_pos,
                        attributeNegative=a_neg,
                        evidence=ev[:400],
                    )
                )
    return tradeoffs


def build_architecture_summaries(sensitivities: List[ComponentSensitivity], tradeoffs: List[Tradeoff],
                                 top_k: int = 5) -> List[ArchitectureSummary]:
    """
    Create summary reports for each architecture, highlighting top sensitivities and tradeoffs.

    :param sensitivities: List of all component sensitivities across architectures
    :param tradeoffs: List of all detected tradeoffs across architectures
    :param top_k:  Maximum number of top sensitivities to include per architecture (default: 5)
    :return: List of ArchitectureSummary objects (one per architecture)
    """
    # group sensitivities and tradeoffs by architecture ID
    by_architecture_sensitivity = defaultdict(list)
    by_architecture_tradeoff = defaultdict(list)

    for sensitivity in sensitivities:
        by_architecture_sensitivity[sensitivity.architectureId].append(sensitivity)
    for tradeoff in tradeoffs:
        by_architecture_tradeoff[tradeoff.architectureId].append(tradeoff)

    # create summary for each architecture
    summaries: List[ArchitectureSummary] = []
    for archtecture_id, sensitivities_list in by_architecture_sensitivity.items():
        # sort sensitivities by magnitude and take top K
        sensitivities_sorted = sorted(sensitivities_list, key=lambda x: x.sensitivity, reverse=True)[:top_k]
        summaries.append(
            ArchitectureSummary(
                architectureId=archtecture_id,
                topSensitivities=sensitivities_sorted,
                tradeoffs=by_architecture_tradeoff.get(archtecture_id, [])
            )
        )

    return summaries
