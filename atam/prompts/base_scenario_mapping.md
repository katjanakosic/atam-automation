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
- strength and confidence are floats in [0,1].
- explanation must be short (<= 200 characters) and must reference a concrete architecture fact: responsibility,
  technology, or an interaction path.

{format_instructions}
