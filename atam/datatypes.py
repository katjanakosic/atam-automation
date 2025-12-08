from enum import Enum

from pydantic import BaseModel, Field


class Impact(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

    def numeric_value(self):
        match self:
            case "low": return 1
            case "medium": return 2
            case "high": return 3
        raise ValueError(f"Impact {self} is not a valid value")


class QualityEvaluationScenario(BaseModel):
    name: str = Field()
    attribute: str = Field()
    environment: str = Field()
    stimulus: str = Field()
    response: str = Field()


class ScenarioMapping(BaseModel):
    component: str = Field(description="The relevant Component of the scenario")
    scenario: str = Field(exclude=True)
    role: str = Field(description="Describe why the component impacts the quality attribute")
    impact: Impact = Field(description="The severity of the impact")
    positive: bool = Field(description="Whether the component contributes to the quality attribute or imposes it")
