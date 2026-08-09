# Module 3 — Agent Safety & Guardrails

**Goal:** make the agent fail *safely* — block bad inputs, validate outputs, and
constrain what tools can do.

## Why
Agents take untrusted input and can take actions. Without guardrails you risk
prompt injection, data leaks, unsafe actions, and broken structured output.

## What's here
```
guardrails.py   # input & output guards + a tool allowlist
test_guardrails.py  # pytest examples
```

## Run it
```bash
python 03-agent-safety-guardrails/guardrails.py     # demo
pytest 03-agent-safety-guardrails/                  # tests
```

## The three layers
1. **Input guards** — before the model
   - PII detection/redaction
   - Prompt-injection / jailbreak pattern detection
   - Length & content limits
2. **Output guards** — after the model, before the user
   - Schema/format validation (structured output)
   - Toxicity / policy checks
   - Groundedness (no hallucinated facts/citations)
3. **Action guards** — around tools
   - Allowlist of callable tools
   - Argument validation + rate limits + timeouts
   - Human-in-the-loop for high-risk actions

## Threat model (know your enemies)
- **Prompt injection** — malicious text tells the model to ignore rules.
- **Data exfiltration** — model coaxed into leaking secrets/other users' data.
- **Excessive agency** — model takes destructive actions unprompted.
- **Insecure output handling** — model output executed/rendered unsafely.

## Frameworks
- **Guardrails AI** — validators + re-ask loops
- **NeMo Guardrails** — dialog/flow rails
- **Llama Guard / prompt-shields** — classifier-based moderation

## Exercises
1. Add a regex + classifier hybrid injection detector.
2. Enforce a JSON schema on tool arguments before execution.
3. Add a "require confirmation" wrapper for destructive tools.
4. Log every blocked request (tie into Module 4).

## Definition of done
- [ ] Known injection strings are blocked
- [ ] Output validated against a schema
- [ ] Only allowlisted tools can run
- [ ] Blocks are logged, not silently dropped
