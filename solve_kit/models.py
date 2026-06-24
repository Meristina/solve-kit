"""Model resolution — the grade → model mapping for the OpenAI Agents SDK port.

Provider-agnostic by env var (defaults keep the original OpenAI behavior, so this is
non-breaking):

  SOLVE_KIT_ELITE_MODEL     elite tier  (🎖️)  default: "gpt-5"
  SOLVE_KIT_STANDARD_MODEL  standard    (🔵)  default: "gpt-5-mini"

To target a non-OpenAI provider, install the LiteLLM extra
(`pip install "openai-agents[litellm]"`) and set a `litellm/<provider>/<model>` string,
e.g.:
  export SOLVE_KIT_ELITE_MODEL="litellm/anthropic/claude-opus-4-20250514"
  export SOLVE_KIT_STANDARD_MODEL="litellm/anthropic/claude-3-5-sonnet-20241022"
or Gemini: "litellm/gemini/gemini-2.0-flash". The SDK routes any `litellm/...` model
string through the LiteLLM extension; plain strings (e.g. "gpt-5") use OpenAI directly.

The grade itself (which unit is elite vs standard) stays fixed in each agent's
definition — only the concrete model behind each grade is configurable here.
"""

import os

ELITE = os.getenv("SOLVE_KIT_ELITE_MODEL", "gpt-5")
STANDARD = os.getenv("SOLVE_KIT_STANDARD_MODEL", "gpt-5-mini")
