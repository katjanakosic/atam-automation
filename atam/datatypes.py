from enum import Enum
from typing import List, Optional, Dict, Literal
from pydantic import BaseModel, Field


# Input Data Types

class Scenario(BaseModel):
    id: str = Field(..., description="Scenario ID")
    name: str
    qualityAttribute: str
    environment: str
    stimulus: str
    response: str

class Component(BaseModel):
    name: str
    type: str
    responsibilities: List[str] = []
    technologies: List[str] = []
    interactsWith: List[str] = []

class Architecture(BaseModel):
    id: str
    domain: str
    architecturePattern: str
    patternCharacteristics: Dict[str, List[str]] = Field(default_factory=dict)
    components: List[Component]
    infrastructure: List[dict] = Field(default_factory=list)


# Mapping Output Types

Strength = Literal[0.1, 0.3, 0.5, 0.7, 0.9]
Confidence = Literal[0.2, 0.4, 0.6, 0.8, 1.0]

class EffectSign(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"

class Effect(BaseModel):
    effectSign: EffectSign
    strength: Strength = Field(..., description="Magnitude of impact (discrete scale)")
    confidence: Confidence = Field(..., description="Evidence-based confidence (discrete scale)")
    # traceable grounding
    evidence: List[str] = Field(
        ...,
        min_length=1,
        max_length=3,
        description="1–3 explicit architecture facts (responsibility/tech) or an interaction path using component names"
    )
    explanation: str = Field(..., description="Short grounded explanation")

class ComponentImpact(BaseModel):
    component: str = Field(..., description="Component name exact as in architecture")
    attribute: str = Field(..., description="Quality attribute for underlying scenario")
    effects: List[Effect] = Field(default_factory=list)

class ScenarioArchitectureMapping(BaseModel):
    architectureId: str
    scenarioId: str
    qualityAttribute: str
    componentImpacts: List[ComponentImpact] = Field(default_factory=list)

# Metrics

class ComponentSensitivity(BaseModel):
    architectureId: str
    component: str
    attribute: str
    sensitivity: float = Field(..., ge=0.0, le=1.0)

class Tradeoff(BaseModel):
    architectureId: str
    component: str
    attributePositive: str
    attributeNegative: str
    evidence: str = Field(..., description="Short explanation of why this is a trade-off")

class ArchitectureSummary(BaseModel):
    architectureId: str
    topSensitivities: List[ComponentSensitivity] = Field(default_factory=list)
    tradeoffs: List[Tradeoff] = Field(default_factory=list)