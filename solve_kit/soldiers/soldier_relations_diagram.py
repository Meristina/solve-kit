"""
SOLDIER (ELITE) — Interrelationship Digraph (OpenAI Agents SDK port)

Mirror of: ../../agents/soldier-relations-diagram.md
         (+ skill ../../skills/relations-diagram/SKILL.md)
Maps which factors influence which, counts in/out degree, and identifies driving
causes (high out-degree, leverage) vs outcomes (high in-degree). Every link
justified; factual links web-sourced or flagged.

Elite = heavier model (full gpt-5): reasoning over a causal influence network.
"""

from agents import Agent, WebSearchTool
from ..models import ELITE

RELATIONS_INSTRUCTIONS = """
You are an ELITE relations-diagram soldier (interrelationship digraph). Given a set
of candidate causes/factors, reason about causal influence between them and find
the DRIVING causes vs the outcomes.

Procedure:
1) List 5-12 factors (label A, B, C...). If too many, cluster first.
2) For every pair, decide X->Y, Y->X, or neither; pick ONE dominant direction (or
   mark bidirectional + dominant side). Write a one-line reason per arrow; cite a
   source if factual, else flag "[hypothèse]".
3) Count out-degree (influences others) and in-degree (influenced) per factor.
4) Classify: highest out-degree (low in) = DRIVER/root cause (leverage); highest
   in-degree = OUTCOME/symptom.
5) Rank drivers by leverage — these are what Phase 3 should target.

Rules: justify every arrow; deliberate direction per pair; drivers/outcomes come
from the COUNTS, not intuition (show numbers). Find drivers only — no new causes,
no solutions. Mirror the user's language. Return: the link list with reasons, the
in/out-degree table, ranked driving causes, key outcomes, and sources/hypotheses.
"""

soldier_relations_diagram = Agent(
    name="soldier_relations_diagram",
    handoff_description="Finds driving causes via influence-network analysis (relations diagram, elite).",
    instructions=RELATIONS_INSTRUCTIONS,
    tools=[WebSearchTool()],  # internet to evidence influence links
    model=ELITE,  # elite: reasoning over a causal network
)
