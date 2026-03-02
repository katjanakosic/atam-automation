import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { QualityAttributeBadge } from "@/components/quality-attribute-badge"
import { SensitivityBar } from "@/components/sensitivity-bar"
import type { ComponentSensitivity } from "@/lib/types"
import { formatArchitectureId } from "@/lib/constants"

interface SensitivityTableProps {
  sensitivities: ComponentSensitivity[]
}

function SensitivityRows({
  sensitivities,
  showArchitecture,
}: {
  sensitivities: ComponentSensitivity[]
  showArchitecture: boolean
}) {
  const sorted = [...sensitivities].sort(
    (a, b) => b.sensitivity - a.sensitivity
  )

  return (
    <div className="rounded-md border overflow-x-auto">
      <Table>
        <TableHeader>
          <TableRow>
            {showArchitecture && <TableHead>Architecture</TableHead>}
            <TableHead>Component</TableHead>
            <TableHead>Quality Attribute</TableHead>
            <TableHead className="text-right">Sensitivity</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {sorted.map((s, i) => (
            <TableRow key={i}>
              {showArchitecture && (
                <TableCell className="text-sm">
                  {formatArchitectureId(s.architectureId)}
                </TableCell>
              )}
              <TableCell className="font-medium text-sm">
                {s.component}
              </TableCell>
              <TableCell>
                <QualityAttributeBadge attribute={s.attribute} />
              </TableCell>
              <TableCell className="text-right">
                <SensitivityBar value={s.sensitivity} className="justify-end" />
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  )
}

export function SensitivityTable({ sensitivities }: SensitivityTableProps) {
  const architectureIds = [
    ...new Set(sensitivities.map((s) => s.architectureId)),
  ]

  return (
    <Tabs defaultValue="all" className="w-full">
      <TabsList className="mb-4">
        <TabsTrigger value="all">All Architectures</TabsTrigger>
        {architectureIds.map((id) => (
          <TabsTrigger key={id} value={id}>
            {formatArchitectureId(id)}
          </TabsTrigger>
        ))}
      </TabsList>

      <TabsContent value="all">
        <SensitivityRows sensitivities={sensitivities} showArchitecture />
      </TabsContent>

      {architectureIds.map((id) => (
        <TabsContent key={id} value={id}>
          <SensitivityRows
            sensitivities={sensitivities.filter((s) => s.architectureId === id)}
            showArchitecture={false}
          />
        </TabsContent>
      ))}
    </Tabs>
  )
}
