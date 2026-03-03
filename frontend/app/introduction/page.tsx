import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Separator } from "@/components/ui/separator"
import { PageNavigation } from "@/components/page-navigation"
import { PIPELINE_STEPS } from "@/lib/constants"

export default function IntroductionPage() {
  return (
    <div className="mx-auto max-w-3xl px-6 py-10 space-y-10">
      {/* What is ATAM? */}
      <section className="space-y-4">
        <h2 className="text-2xl font-bold tracking-tight">What is ATAM?</h2>
        <p className="text-muted-foreground leading-relaxed">
          The{" "}
          <strong className="text-foreground">
            Architecture Tradeoff Analysis Method (ATAM)
          </strong>{" "}
          is a structured methodology for evaluating software architectures
          against quality-attribute requirements. It systematically identifies
          how architectural decisions affect quality attributes and where
          those decisions create tradeoffs between competing concerns.
        </p>
        <p className="text-muted-foreground leading-relaxed">
          ATAM surfaces two key types of architectural insights:
        </p>
        <div className="flex flex-wrap gap-2">
          <Badge
            variant="outline"
            className="bg-amber-50 text-amber-800 border-amber-300"
          >
            Sensitivity Points
          </Badge>
          <span className="text-sm text-muted-foreground self-center">
            — components whose architectural properties significantly influence
            a quality attribute
          </span>
        </div>
        <div className="flex flex-wrap gap-2">
          <Badge
            variant="outline"
            className="bg-violet-50 text-violet-800 border-violet-300"
          >
            Tradeoff Points
          </Badge>
          <span className="text-sm text-muted-foreground self-center">
            — components where improving one quality attribute negatively
            affects another
          </span>
        </div>
      </section>

      <Separator />

      {/* What does this tool do? */}
      <section className="space-y-4">
        <h2 className="text-2xl font-bold tracking-tight">
          What Does This Tool Do?
        </h2>
        <p className="text-muted-foreground leading-relaxed">
          This tool automates the core analytical steps of ATAM using large
          language models (LLMs). Given a set of quality-attribute scenarios and
          candidate architecture definitions, it produces structured,
          evidence-grounded evaluations. Thus, it is replacing a manual expert workshop
          with a reproducible pipeline.
        </p>

        <h3 className="text-lg font-semibold mt-6">Pipeline Overview</h3>
        <div className="grid gap-3">
          {PIPELINE_STEPS.map((step) => (
            <Card key={step.number}>
              <CardHeader className="pb-2 flex flex-row items-center gap-3">
                <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-primary text-primary-foreground text-sm font-bold">
                  {step.number}
                </div>
                <CardTitle className="text-base">{step.title}</CardTitle>
              </CardHeader>
              <CardContent className="pl-17">
                <p className="text-sm text-muted-foreground">
                  {step.description}
                </p>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>

      <Separator />

      {/* Purpose of this evaluation */}
      <section className="space-y-4">
        <h2 className="text-2xl font-bold tracking-tight">
          Purpose of This Evaluation
        </h2>
        <p className="text-muted-foreground leading-relaxed">
          You are being asked to review the automated ATAM pipeline as an architecture
          expert. The following pages will present:
        </p>
        <ol className="list-decimal list-inside space-y-2 text-sm text-muted-foreground">
          <li>
            <strong className="text-foreground">Input</strong> — The
            quality-attribute scenarios and candidate architectures that were
            provided to the tool.
          </li>
          <li>
            <strong className="text-foreground">Output</strong> — The tool's
            analysis results: architecture summaries, component sensitivity
            scores, and detected tradeoffs.
          </li>
        </ol>
        <p className="text-muted-foreground leading-relaxed">
          Your feedback will help validate whether the automated pipeline
          produces architecturally sound and useful results compared to a
          traditional expert-driven ATAM workshop.
        </p>
      </section>

      <PageNavigation nextHref="/input" nextLabel="View Input" />
    </div>
  )
}
