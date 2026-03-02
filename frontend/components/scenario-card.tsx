import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { QualityAttributeBadge } from "@/components/quality-attribute-badge"
import type { Scenario } from "@/lib/types"

interface ScenarioCardProps {
  scenario: Scenario
}

export function ScenarioCard({ scenario }: ScenarioCardProps) {
  return (
    <Card>
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between gap-2">
          <CardTitle className="text-base font-semibold">
            {scenario.id}
          </CardTitle>
          <QualityAttributeBadge attribute={scenario.qualityAttribute} />
        </div>
        <p className="text-sm text-muted-foreground">{scenario.name}</p>
      </CardHeader>
      <CardContent className="space-y-3 text-sm">
        {scenario.stimulusSource && (
          <div>
            <span className="text-muted-foreground font-medium">Source: </span>
            <span>{scenario.stimulusSource}</span>
          </div>
        )}
        <div>
          <span className="text-muted-foreground font-medium">Stimulus: </span>
          <span>{scenario.stimulus}</span>
        </div>
        {scenario.environment && (
          <div>
            <span className="text-muted-foreground font-medium">
              Environment:{" "}
            </span>
            <span>{scenario.environment}</span>
          </div>
        )}
        <div>
          <span className="text-muted-foreground font-medium">Response: </span>
          <span>{scenario.response}</span>
        </div>
        {scenario.responseMeasure && (
          <div>
            <span className="text-muted-foreground font-medium">Measure: </span>
            <span>{scenario.responseMeasure}</span>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
