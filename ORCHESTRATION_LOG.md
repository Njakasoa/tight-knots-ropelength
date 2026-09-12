# Orchestration audit

Started 2026-09-12 UTC; local date crossed into 2026-09-13 (UTC+3).
Bibliography cutoff remains 2026-09-12, as requested.

Source: https://github.com/donvito/codex-astra-luna-orchestrator
Project-local Pro configuration copied by the inspected upstream setup.sh.
The profile label describes configuration; it is not evidence of subscription tier.
No global configuration changed. This does not retroactively change the running root.
Official configuration reference: https://learn.chatgpt.com/docs/agent-configuration/subagents

Runtime tool advertises four total concurrent slots including root, so waves have
at most three children. Runtime limits take precedence over installed preferences.
The root is identified by session instructions as GPT-6-based Codex; precise effective
root model slug and effort are not independently exposed in tool results. Do not infer
them from config.toml. Reviewer requests will explicitly select gpt-6-astra.

| Agent | Requested model | Requested effort | Evidence/status |
|---|---|---|---|
| researcher_frontier | gpt-5.6-luna | high | successful spawn /root/researcher_frontier |
| researcher_recent | gpt-5.6-luna | high | successful spawn /root/researcher_recent |
| explorer | gpt-5.6-luna | high | successful spawn /root/explorer |

The first wave preceded reading upstream skill and used high. Subsequent routine
spawns follow installed max. Successful tool dispatch is evidence of acceptance,
not independent attestation of backend routing. No unsupported reasoning is claimed.

Ownership: frontier owns NORMALIZATION and CLASSICAL_FRONTIER; recent researcher
owns RECENT_TORUS_AUDIT; explorer owns environment/software audit and dependencies;
root owns strategy, integration, mathematical synthesis and milestone decisions.
