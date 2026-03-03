import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Separator } from "@/components/ui/separator"
import type { Architecture } from "@/lib/types"
import { formatArchitectureId } from "@/lib/constants"

interface ArchitectureViewProps {
  architectures: Architecture[]
}

export function ArchitectureView({ architectures }: ArchitectureViewProps) {
  return (
    <Tabs defaultValue={architectures[0]?.id} className="w-full">
      <TabsList className="w-full justify-start flex-wrap h-auto gap-1 p-1">
        {architectures.map((arch) => (
          <TabsTrigger key={arch.id} value={arch.id} className="text-sm">
            {formatArchitectureId(arch.id)}
          </TabsTrigger>
        ))}
      </TabsList>

      {architectures.map((arch) => (
        <TabsContent key={arch.id} value={arch.id} className="space-y-6 mt-4">
          <div className="space-y-2">
            <p className="text-sm">
              <span className="font-medium text-muted-foreground">
                Pattern:{" "}
              </span>
              {arch.architecturePattern}
            </p>
          </div>

          <div className="grid gap-4 sm:grid-cols-2">
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-green-700">
                  Advantages
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="list-disc list-inside space-y-1 text-sm">
                  {arch.patternCharacteristics.advantages.map((adv, i) => (
                    <li key={i}>{adv}</li>
                  ))}
                </ul>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-red-700">
                  Disadvantages
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="list-disc list-inside space-y-1 text-sm">
                  {arch.patternCharacteristics.disadvantages.map((dis, i) => (
                    <li key={i}>{dis}</li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          </div>

          <Separator />

          <div>
            <h4 className="text-sm font-semibold mb-3">
              Components ({arch.components.length})
            </h4>
            <div className="rounded-md border overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead className="w-40">Component</TableHead>
                    <TableHead className="w-25">Type</TableHead>
                    <TableHead className="w-45">Interacts With</TableHead>
                    <TableHead>Responsibilities</TableHead>
                    <TableHead className="w-40">Technologies</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {arch.components.map((comp) => (
                    <TableRow key={comp.name}>
                      <TableCell className="font-medium text-sm">
                        {comp.name}
                      </TableCell>
                      <TableCell>
                        <Badge variant="secondary" className="text-xs">
                          {comp.type}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        <div className="flex flex-wrap gap-1">
                          {comp.interactsWith.map((iw) => (
                            <Badge
                              key={iw}
                              variant="secondary"
                              className="text-xs font-normal"
                            >
                              {iw}
                            </Badge>
                          ))}
                        </div>
                      </TableCell>
                      <TableCell>
                        <ul className="list-disc list-inside text-sm space-y-0.5">
                          {comp.responsibilities.map((r, i) => (
                            <li key={i}>{r}</li>
                          ))}
                        </ul>
                      </TableCell>
                      <TableCell>
                        <div className="flex flex-wrap gap-1">
                          {comp.technologies.map((t) => (
                            <Badge
                              key={t}
                              variant="outline"
                              className="text-xs"
                            >
                              {t}
                            </Badge>
                          ))}
                        </div>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          </div>
        </TabsContent>
      ))}
    </Tabs>
  )
}
