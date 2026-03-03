import { Badge } from "@/components/ui/badge"
import { Card, CardContent } from "@/components/ui/card"
import { PageNavigation } from "@/components/page-navigation"
import { SummaryCard } from "@/components/summary-card"
import { loadSummaries, loadRunIndex } from "@/lib/data"

export default function OutputPage() {
  const summaries = loadSummaries()
  const runIndex = loadRunIndex()

  return (
    <div className="mx-auto max-w-6xl px-6 py-10 space-y-10">
      {/* Page header */}
      <div>
        <h2 className="text-2xl font-bold tracking-tight">
          Output: Architecture Summaries
        </h2>
        <p className="text-muted-foreground mt-1">
          Side-by-side comparison of the automated ATAM pipeline results for
          each candidate architecture.
        </p>
      </div>

      {/* Run metadata */}
      <Card>
        <CardContent className="flex flex-wrap items-center gap-x-6 gap-y-2 py-3 text-sm">
          <div className="flex items-center gap-1.5">
            <span className="text-muted-foreground">Domain:</span>
            <Badge variant="secondary">{runIndex.domain}</Badge>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="text-muted-foreground">Scenarios:</span>
            <Badge variant="outline">{runIndex.counts.scenarios}</Badge>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="text-muted-foreground">Architectures:</span>
            <Badge variant="outline">{runIndex.counts.architectures}</Badge>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="text-muted-foreground">Mappings:</span>
            <Badge variant="outline">
              {runIndex.counts.mappingsProduced}/
              {runIndex.counts.mappingsExpected}
            </Badge>
          </div>
        </CardContent>
      </Card>

      {/* Architecture summaries side-by-side */}
      <div className="grid gap-6 lg:grid-cols-2">
        {summaries.map((summary) => (
          <SummaryCard key={summary.architectureId} summary={summary} />
        ))}
      </div>

      <PageNavigation previousHref="/input" previousLabel="View Input" />
    </div>
  )
}
