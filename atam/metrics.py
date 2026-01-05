from collections import defaultdict
from typing import List, Dict, Tuple

from atam.datatypes import ScenarioArchitectureMapping, ComponentSensitivity


def compute_component_sensitivities(mappings: List[ScenarioArchitectureMapping]) -> List[ComponentSensitivity]:
    """
        sensitivity(architecture, component, attribute) = avg_over_scenarios(strength * confidence)
        Direction (positive/negative) is ignored for sensitivity magnitude
    """
    bucket: Dict[Tuple[str, str, str], List[float]] = defaultdict(list)

    for mapping in mappings:
        architecture_id = mapping.architecture_id
        attribute = mapping.qualityAttribute
        for impact in mapping.componentImpacts:
            for effect in impact.effects:
                score = float(effect.strength) * float(effect.confidence)
                bucket[(architecture_id, impact.component, attribute)].append(score)

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
