// ─── Inputs ───
export interface Scenario {
  id: string
  name: string
  qualityAttribute: string
  stimulus: string
  stimulusSource?: string
  response: string
  responseMeasure?: string
  environment?: string
}

export interface ArchitectureComponent {
  name: string
  type: string
  responsibilities: string[]
  technologies: string[]
  interactsWith: string[]
}

export interface Architecture {
  id: string
  domain: string
  architecturePattern: string
  patternCharacteristics: {
    advantages: string[]
    disadvantages: string[]
  }
  components: ArchitectureComponent[]
  infrastructure?: {
    name: string
    type: string
    details: string
  }[]
}

// ─── Outputs ───
export interface ComponentSensitivity {
  architectureId: string
  component: string
  attribute: string
  sensitivity: number
}

export interface Tradeoff {
  architectureId: string
  component: string
  attributePositive: string
  attributeNegative: string
  evidence: string
}

export interface ArchitectureSummary {
  architectureId: string
  topSensitivities: ComponentSensitivity[]
  tradeoffs: Tradeoff[]
}

export interface RunIndex {
  domain: string
  inputs: {
    scenarios: string
    architecturesDir: string
    prompt: string
  }
  llm: {
    provider: string
    ollama: unknown
    openrouter: {
      base_url: string
      model: string
    } | null
  }
  outputs: {
    mappingsDir: string
    sensitivities: string
    tradeoffs: string
    summaries: string
  }
  counts: {
    scenarios: number
    architectures: number
    mappingsExpected: number
    mappingsProduced: number
  }
}
