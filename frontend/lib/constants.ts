export const QUALITY_ATTRIBUTE_COLORS: Record<
  string,
  { bg: string; text: string; border: string }
> = {
  performance: {
    bg: "bg-blue-100",
    text: "text-blue-800",
    border: "border-blue-300",
  },
  security: {
    bg: "bg-red-100",
    text: "text-red-800",
    border: "border-red-300",
  },
  modifiability: {
    bg: "bg-amber-100",
    text: "text-amber-800",
    border: "border-amber-300",
  },
  availability: {
    bg: "bg-green-100",
    text: "text-green-800",
    border: "border-green-300",
  },
  scalability: {
    bg: "bg-purple-100",
    text: "text-purple-800",
    border: "border-purple-300",
  },
  usability: {
    bg: "bg-pink-100",
    text: "text-pink-800",
    border: "border-pink-300",
  },
  reliability: {
    bg: "bg-teal-100",
    text: "text-teal-800",
    border: "border-teal-300",
  },
  maintainability: {
    bg: "bg-orange-100",
    text: "text-orange-800",
    border: "border-orange-300",
  },
  testability: {
    bg: "bg-cyan-100",
    text: "text-cyan-800",
    border: "border-cyan-300",
  },
  interoperability: {
    bg: "bg-indigo-100",
    text: "text-indigo-800",
    border: "border-indigo-300",
  },
}

const DEFAULT_QA_COLOR = {
  bg: "bg-gray-100",
  text: "text-gray-800",
  border: "border-gray-300",
}

export function getQAColor(attribute: string) {
  const key = attribute.toLowerCase().trim()
  return QUALITY_ATTRIBUTE_COLORS[key] ?? DEFAULT_QA_COLOR
}

export const SENSITIVITY_THRESHOLDS = {
  high: 0.5,
  medium: 0.3,
} as const

export function getSensitivityColor(value: number): string {
  if (value >= SENSITIVITY_THRESHOLDS.high) return "#22c55e"  // green-500
  if (value >= SENSITIVITY_THRESHOLDS.medium) return "#eab308" // yellow-500
  return "#9ca3af" // gray-400
}

export const PIPELINE_STEPS = [
  {
    number: 1,
    title: "Load Input",
    description:
      "Read scenarios and candidate architecture definitions from structured JSON files.",
  },
  {
    number: 2,
    title: "Create Scenario x Architecture Mapping",
    description:
      "For each scenario × architecture pair, prompt the LLM to identify impacted components with strength, confidence, effect direction, and grounded evidence.",
  },
  {
    number: 3,
    title: "Compute Sensitivities",
    description:
      "Aggregate component impacts across scenarios to calculate sensitivity scores per (component, quality attribute) pair.",
  },
  {
    number: 4,
    title: "Detect Tradeoffs",
    description:
      "Identify components that positively affect one quality attribute but negatively affect another.",
  },
  {
    number: 5,
    title: "Generate Summaries",
    description:
      "Produce per-architecture summaries ranking the top sensitivity points and listing all detected tradeoffs.",
  },
] as const

export function formatArchitectureId(id: string): string {
  return id.replace(/[-_]/g, " ").replace(/\b\w/g, (c) => c.toUpperCase())
}
