Act as a software architecture evaluation assistant performing an ATAM-like analysis.

Goal: Given one scenario and one candidate architecture, identify which of the architecture's
components are most impacted with respect to the scenario's quality attribute.

INPUT SCENARIO (JSON):
{scenario_json}

CANDIDATE ARCHITECTURE (JSON):
{architecture_json}

Rules:
- Use only component names that exist in the provided architecture JSON.
- Select 3 to 6 components maximum. Choose the most relevant.
- For each selected component, output exactly 1 effect.
- effectSign is "positive" if the component tends to improve/support the quality attribute in this scenario.
  effectSign is "negative" if it tends to harm/limit the quality attribute in this scenario.

Scoring (DISCRETE ONLY; no other numbers allowed):
- strength ∈ {0.1, 0.3, 0.5, 0.7, 0.9}
  0.1 negligible influence
  0.3 minor influence
  0.5 moderate driver
  0.7 major driver
  0.9 dominant driver / likely sensitivity point

- confidence ∈ {0.2, 0.4, 0.6, 0.8, 1.0}  
  0.2 weak grounding; architecture facts unclear / assumed
  0.4 some grounding; indirect evidence
  0.6 grounded in at least ONE explicit architecture fact (responsibility or technology)
  0.8 grounded in at least TWO explicit facts OR ONE explicit interaction path
  1.0 grounded in TWO+ explicit facts AND a direct causal interaction path

Grounding requirement:
- Provide evidence as evidence[] with 1–3 items.
- Each evidence item MUST be directly supported by the architecture JSON:
  - Either quote a responsibility or technology phrase as written, OR
  - Provide an interaction path using component names like "A -> B -> C" where each hop exists in interactsWith.
- explanation must be <= 200 characters and must be consistent with evidence[].

Return ONLY valid JSON. No markdown. No commentary. No preamble.

{format_instructions}
