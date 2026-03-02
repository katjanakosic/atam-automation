import Link from "next/link"
import { Button } from "@/components/ui/button"
import { ChevronLeft } from "lucide-react"
import { SensitivityTable } from "@/components/sensitivity-table"
import { loadSensitivities } from "@/lib/data"

export default function SensitivitiesPage() {
  const sensitivities = loadSensitivities()

  return (
    <div className="mx-auto max-w-6xl px-6 py-10 space-y-8">
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="sm" asChild>
          <Link href="/output">
            <ChevronLeft className="mr-1 h-4 w-4" />
            Back to Summary
          </Link>
        </Button>
      </div>

      <div>
        <h2 className="text-2xl font-bold tracking-tight">
          Component Sensitivities
        </h2>
        <p className="text-muted-foreground mt-1">
          Full list of component sensitivity scores across all architectures,
          sorted by impact. A high sensitivity means the component is a dominant
          driver of that quality attribute.
        </p>
      </div>

      <SensitivityTable sensitivities={sensitivities} />
    </div>
  )
}
