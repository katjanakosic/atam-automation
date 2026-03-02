import fs from "fs"
import path from "path"
import type {
  Scenario,
  Architecture,
  ComponentSensitivity,
  Tradeoff,
  ArchitectureSummary,
  RunIndex,
} from "./types"

const DOMAIN = "online-learning-platform-system"
const RUN = "run-20260301-230914"

const DATA_DIR = path.join(process.cwd(), "..", "data", DOMAIN)
const OUTPUT_DIR = path.join(process.cwd(), "..", "outputs", DOMAIN, RUN)

export function loadScenarios(): Scenario[] {
  const raw = fs.readFileSync(path.join(DATA_DIR, "scenarios.json"), "utf-8")
  return JSON.parse(raw)
}

export function loadArchitectures(): Architecture[] {
  const dir = path.join(DATA_DIR, "architectures")
  const files = fs
    .readdirSync(dir)
    .filter((f) => f.endsWith(".json"))
    .sort()
  return files.map((f) =>
    JSON.parse(fs.readFileSync(path.join(dir, f), "utf-8"))
  )
}

export function loadSensitivities(): ComponentSensitivity[] {
  const raw = fs.readFileSync(
    path.join(OUTPUT_DIR, "metrics", "component_sensitivities.json"),
    "utf-8"
  )
  return JSON.parse(raw)
}

export function loadTradeoffs(): Tradeoff[] {
  const raw = fs.readFileSync(
    path.join(OUTPUT_DIR, "metrics", "tradeoffs.json"),
    "utf-8"
  )
  return JSON.parse(raw)
}

export function loadSummaries(): ArchitectureSummary[] {
  const raw = fs.readFileSync(
    path.join(OUTPUT_DIR, "summary", "architecture_summaries.json"),
    "utf-8"
  )
  return JSON.parse(raw)
}

export function loadRunIndex(): RunIndex {
  const raw = fs.readFileSync(path.join(OUTPUT_DIR, "run_index.json"), "utf-8")
  return JSON.parse(raw)
}
