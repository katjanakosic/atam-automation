import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { QualityAttributeBadge } from "@/components/quality-attribute-badge"
import { Separator } from "@/components/ui/separator"
import type { Tradeoff } from "@/lib/types"
import { formatArchitectureId } from "@/lib/constants"

interface TradeoffCardProps {
  tradeoff: Tradeoff
}

export function TradeoffCard({ tradeoff }: TradeoffCardProps) {
  const evidenceParts = tradeoff.evidence.split("|").map((p) => p.trim())

  return (
    <Card>
      <CardHeader className="pb-3">
        <CardTitle className="text-base font-semibold">
          {tradeoff.component}
        </CardTitle>
        <p className="text-sm text-muted-foreground">
          {formatArchitectureId(tradeoff.architectureId)}
        </p>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex items-center gap-3 flex-wrap">
          <div className="flex items-center gap-1.5">
            <span className="text-green-700 font-medium text-sm">
              ✓ Supports
            </span>
            <QualityAttributeBadge attribute={tradeoff.attributePositive} />
          </div>
          <span className="text-muted-foreground">→</span>
          <div className="flex items-center gap-1.5">
            <span className="text-red-700 font-medium text-sm">✗ Hinders</span>
            <QualityAttributeBadge attribute={tradeoff.attributeNegative} />
          </div>
        </div>

        <Separator />

        <div className="space-y-1.5">
          <h5 className="text-xs font-semibold uppercase tracking-wide text-muted-foreground">
            Evidence
          </h5>
          {evidenceParts.map((part, i) => {
            const isPositive = part.startsWith("+")
            const isNegative = part.startsWith("-")
            return (
              <p
                key={i}
                className={`text-sm ${
                  isPositive
                    ? "text-green-700"
                    : isNegative
                    ? "text-red-700"
                    : "text-foreground"
                }`}
              >
                {part}
              </p>
            )
          })}
        </div>
      </CardContent>
    </Card>
  )
}
