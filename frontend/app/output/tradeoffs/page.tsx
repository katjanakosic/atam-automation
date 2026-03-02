import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Separator } from "@/components/ui/separator"
import { ChevronLeft } from "lucide-react"
import { TradeoffCard } from "@/components/tradeoff-card"
import { loadTradeoffs } from "@/lib/data"
import { formatArchitectureId } from "@/lib/constants"

export default function TradeoffsPage() {
  const tradeoffs = loadTradeoffs()

  const grouped = tradeoffs.reduce<Record<string, typeof tradeoffs>>(
    (acc, t) => {
      if (!acc[t.architectureId]) acc[t.architectureId] = []
      acc[t.architectureId].push(t)
      return acc
    },
    {}
  )

  const architectureIds = Object.keys(grouped)

  return (
    <div className="mx-auto max-w-5xl px-6 py-10 space-y-8">
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="sm" asChild>
          <Link href="/output">
            <ChevronLeft className="mr-1 h-4 w-4" />
            Back to Summary
          </Link>
        </Button>
      </div>

      <div>
        <h2 className="text-2xl font-bold tracking-tight">Tradeoffs</h2>
        <p className="text-muted-foreground mt-1">
          Components where improving one quality attribute negatively affects
          another. Each tradeoff includes evidence from the LLM analysis.
        </p>
      </div>

      {architectureIds.map((archId, i) => (
        <section key={archId} className="space-y-4">
          {i > 0 && <Separator />}
          <h3 className="text-lg font-semibold">
            {formatArchitectureId(archId)}
          </h3>
          <div className="grid gap-4 sm:grid-cols-2">
            {grouped[archId].map((tradeoff, j) => (
              <TradeoffCard key={j} tradeoff={tradeoff} />
            ))}
          </div>
        </section>
      ))}
    </div>
  )
}
