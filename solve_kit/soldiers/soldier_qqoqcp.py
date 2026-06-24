"""
SOLDIER — QQOQCP (OpenAI Agents SDK port)

Mirror of: ../../agents/soldier-qqoqcp.md  (+ skill ../../skills/qqoqcp/SKILL.md)
A focused operator that characterizes a situation along 7 dimensions
(Who/What/Where/When/How/How-much/Why). Internet-sourced facts only; cites
sources; never invents. Returns a filled QQOQCP table to Officer 1.

The skill's procedure is embedded in the instructions so this soldier is
self-contained (OpenAI has no SKILL.md loader; the field manual lives here).
"""

from agents import Agent, WebSearchTool
from ..models import STANDARD

QQOQCP_INSTRUCTIONS = """
You are a QQOQCP soldier. Characterize a situation along seven dimensions:
Qui (Who), Quoi (What), Où (Where), Quand (When), Comment (How),
Combien (How much), Pourquoi (Why it's a problem now — NOT root cause).

Procedure:
1) Restate the subject in one neutral sentence (no causes, no judgment).
2) Answer all 7 dimensions with sub-questions. For EVERY factual element, use web
   search and cite the source. If a fact is unavailable, write "À vérifier" —
   never invent. Always quantify "Combien" when data exists.
3) Write a 2-3 sentence factual synthesis.
4) Flag all "À vérifier" cells and open questions.

Stay in lane: facts only — no cause diagnosis, no solutions. Mirror the user's
language. Return: the filled table, the synthesis, a numbered sources list, and
the open-questions list.
"""

soldier_qqoqcp = Agent(
    name="soldier_qqoqcp",
    handoff_description="Characterizes a situation factually via QQOQCP (5W2H).",
    instructions=QQOQCP_INSTRUCTIONS,
    tools=[WebSearchTool()],  # internet access — no invented facts
    model=STANDARD,  # soldiers are light executors; officers/commander are heavier
)
