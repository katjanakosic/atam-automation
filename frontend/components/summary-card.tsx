import Link from "next/link"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Separator } from "@/components/ui/separator"
import { QualityAttributeBadge } from "@/components/quality-attribute-badge"
import { SensitivityBar } from "@/components/sensitivity-bar"
import { ArrowRight } from "lucide-react"
import type { ArchitectureSummary } from "@/lib/types"
import { formatArchitectureId } from "@/lib/constants"

interface SummaryCardProps {
  summary: ArchitectureSummary
}

export function SummaryCard({ summary }: SummaryCardProps) {
  return (
    <Card className="flex flex-col">
      <CardHeader>
        <CardTitle className="text-lg">
          {formatArchitectureId(summary.architectureId)}
        </CardTitle>
      </CardHeader>
      <CardContent className="flex-1 space-y-6">
        {/* Top Sensitivities */}
        <div className="space-y-3">
          <h4 className="text-sm font-semibold">Top Sensitivity Points</h4>
          <div className="space-y-2">
            {summary.topSensitivities.map((s, i) => (
              <div key={i} className="flex items-center justify-between gap-2">
                <div className="flex items-center gap-2 min-w-0">
                  <span className="text-sm font-medium truncate">
                    {s.component}
                  </span>
                  <QualityAttributeBadge attribute={s.attribute} />
                </div>
                <SensitivityBar value={s.sensitivity} />
              </div>
            ))}
          </div>
          <Button variant="link" className="px-0 h-auto text-sm" asChild>
            <Link href="/output/sensitivities">
              View all sensitivities
              <ArrowRight className="ml-1 h-3 w-3" />
            </Link>
          </Button>
        </div>

        <Separator />

        {/* Tradeoffs */}
        <div className="space-y-3">
          <h4 className="text-sm font-semibold">
            Tradeoffs ({summary.tradeoffs.length})
          </h4>
          {summary.tradeoffs.length === 0 ? (
            <p className="text-sm text-muted-foreground">
              No tradeoffs detected.
            </p>
          ) : (
            <div className="space-y-2">
              {summary.tradeoffs.map((t, i) => (
                <div
                  key={i}
                  className="text-sm flex items-center gap-1.5 flex-wrap"
                >
                  <span className="font-medium">{t.component}:</span>
                  <span className="text-green-700">
                    ✓ {t.attributePositive}
                  </span>
                  <span className="text-muted-foreground">→</span>
                  <span className="text-red-700">✗ {t.attributeNegative}</span>
                </div>
              ))}
            </div>
          )}
          <Button variant="link" className="px-0 h-auto text-sm" asChild>
            <Link href="/output/tradeoffs">
              View all tradeoffs
              <ArrowRight className="ml-1 h-3 w-3" />
            </Link>
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}
