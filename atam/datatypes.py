from enum import Enum
from typing import List, Optional, Dict
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

class EffectSign(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"


class Effect(BaseModel):
    effectSign: EffectSign
    strength: float = Field(..., ge=0.0, le=1.0, description="Magnitude of impact")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Model's confidence level")
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







