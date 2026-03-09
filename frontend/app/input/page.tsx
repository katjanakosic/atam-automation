import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { PageNavigation } from "@/components/page-navigation"
import { ScenarioCard } from "@/components/scenario-card"
import { ArchitectureView } from "@/components/architecture-view"
import { loadScenarios, loadArchitectures } from "@/lib/data"

export default function InputPage() {
  const scenarios = loadScenarios()
  const architectures = loadArchitectures()

  return (
    <div className="mx-auto max-w-6xl px-6 py-10 space-y-10">
      {/* Page header */}
      <div>
        <h2 className="text-2xl font-bold tracking-tight">
          Input Domain: SecuRooms
        </h2>
        <p className="text-muted-foreground mt-1">
          The scenarios and candidate architectures provided to the automated
          ATAM analysis.
        </p>
      </div>

      {/* Scenarios */}
      <section className="space-y-4">
        <div className="flex items-center gap-2">
          <h3 className="text-xl font-semibold">Scenarios</h3>
          <Badge variant="secondary">{scenarios.length}</Badge>
        </div>
        <div className="grid gap-4 sm:grid-cols-2">
          {scenarios.map((scenario) => (
            <ScenarioCard key={scenario.id} scenario={scenario} />
          ))}
        </div>
      </section>

      <Separator />

      {/* Architectures */}
      <section className="space-y-4">
        <div className="flex items-center gap-2">
          <h3 className="text-xl font-semibold">Candidate Architectures</h3>
          <Badge variant="secondary">{architectures.length}</Badge>
        </div>
        <ArchitectureView architectures={architectures} />
      </section>

      <PageNavigation
        previousHref="/introduction"
        previousLabel="Introduction"
        nextHref="/output"
        nextLabel="View Output"
      />
    </div>
  )
}
