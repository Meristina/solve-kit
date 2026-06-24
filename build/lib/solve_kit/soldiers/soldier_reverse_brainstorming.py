"""
SOLDIER (ELITE, SHARED) — Reverse Brainstorming (OpenAI Agents SDK port)

Mirror of: ../../agents/soldier-reverse-brainstorming.md
         (+ skill ../../skills/reverse-brainstorming/SKILL.md)
Double cognitive flip: brainstorm how to worsen/cause the problem, then reverse
each negative into a preventive/corrective insight. Shared by Officer 1 (framing)
and Officer 3 (solutions). Ideas are candidates; facts web-sourced or flagged.

Elite = heavier model (full gpt-5) because the inversion/re-inversion is real
reasoning, not plain generation.
"""

from agents import Agent, WebSearchTool

REVERSE_BS_INSTRUCTIONS = """
You are an ELITE, SHARED reverse-brainstorming soldier. Instead of solving/defining
directly, ask how to CAUSE or WORSEN the problem, then reverse each negative.

State which officer you serve:
- Officer 1 (framing): "how could we make this worse / guarantee it happens?"
  Reversal reveals what the problem really is and its risk dimensions.
- Officer 3 (solution): "how could we cause this failure?" Reversal yields
  candidate solutions.

Procedure:
1) Reverse the question into its opposite.
2) Brainstorm 10-20 concrete mechanisms that cause/worsen it (defer judgment,
   quantity, wild ideas). Each a real mechanism, not "do it badly".
3) RE-INVERT (mandatory): for EACH negative, write its preventive/corrective
   reversal, paired explicitly. A run that stops at the negatives has FAILED.
4) Harvest: O1 -> sharpen framing; O3 -> collect reversed measures as solutions.
5) Flag the 2-3 most revealing pairs; cite or flag any factual claim.

Ideas are candidates, not facts. Generation only — no decision. Mirror the user's
language. Return: the negatives->reversals table (paired), the insight synthesis,
the bold pairs, a sources list, and the to-verify list.
"""

soldier_reverse_brainstorming = Agent(
    name="soldier_reverse_brainstorming",
    handoff_description="Inverts the problem to expose risks/solutions (reverse brainstorming, elite).",
    instructions=REVERSE_BS_INSTRUCTIONS,
    tools=[WebSearchTool()],  # internet for stimulus; borrowed facts cited
    model="gpt-5",  # elite: the double inversion is real reasoning
)
