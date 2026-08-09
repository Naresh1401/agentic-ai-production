# Notes — Agent Safety & Guardrails

## Defense in depth
No single check is enough. Layer heuristics + classifiers + schema validation +
least-privilege tools. Assume any one layer can be bypassed.

## Prompt injection is unsolved
Treat all model input as untrusted, including tool/RAG results (indirect
injection). Mitigations, not cures:
- Keep the system prompt separate; don't let user text override it.
- Least privilege: minimal tools, minimal scopes, minimal data in context.
- Validate/escape model output before executing or rendering it.
- Human-in-the-loop for irreversible actions.

## Structured output safety
- Prefer provider "JSON mode"/function calling + a schema validator.
- On invalid output, **re-ask** with the error, don't crash.

## Moderation
- Classify both input and output (toxicity, self-harm, illegal, PII).
- Log blocks with reason codes for auditing and eval building.

## Least-privilege tools
- Allowlist tools per agent/role.
- Validate arguments against a schema before calling.
- Add per-tool rate limits, timeouts, and idempotency keys.
- Sandbox side effects (dry-run, staging creds) while learning.

## OWASP LLM Top 10 (know these)
LLM01 Prompt injection · LLM02 Insecure output handling · LLM03 Training data
poisoning · LLM06 Sensitive info disclosure · LLM08 Excessive agency. Map each
to a concrete guard in your service.
