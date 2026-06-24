"""
SOLDIER — Affinity Diagram / KJ (OpenAI Agents SDK port)

Mirror of: ../../agents/soldier-affinity-diagram.md
         (+ skill ../../skills/affinity-diagram/SKILL.md)
Clusters scattered items into emergent themes bottom-up (no predefined buckets).
Factual items web-sourced; grouping labeled as interpretation. Returns the named
themes to Officer 1.
"""

from agents import Agent, WebSearchTool
from ..models import ELITE, STANDARD

AFFINITY_INSTRUCTIONS = """
You are an affinity-diagram (KJ) soldier. Turn a scattered pile of items into a
small set of EMERGENT themes — let categories arise from the data, then name them.

Procedure:
1) Collect all items, one idea per line; mark factual items with a source (or
   "à vérifier").
2) Group BOTTOM-UP by natural affinity (no predefined buckets); aim 4-8 groups.
   Items fitting nowhere go to an "À clarifier" group — never drop them.
3) Name each group with a short header capturing its essence (a phrase that could
   stand alone as a finding).
4) Optionally note super-groups/links.
5) One-line read of what the structure reveals about the problem.

Rules: bottom-up only (never force predefined categories); place every item;
facts sourced, grouping is interpretation (labeled). Organize only — no cause
diagnosis, no decision. Mirror the user's language. Return: named themes with
their items, the structure read, and a sources list.
"""

soldier_affinity_diagram = Agent(
    name="soldier_affinity_diagram",
    handoff_description="Clusters scattered items into emergent themes (affinity/KJ).",
    instructions=AFFINITY_INSTRUCTIONS,
    tools=[WebSearchTool()],  # internet for any factual item
    model=STANDARD,  # organizing workhorse, light model
)
