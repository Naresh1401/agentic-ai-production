# Notes — Infrastructure & Cloud Governance

## Why governance, not just deployment
Anyone can `gcloud run deploy`. Governance answers: *who* can change *what*,
*how* it's reviewed, whether it's *compliant* and *tagged*, what it *costs*, and
how you *prove* all of that to an auditor. It scales a team from one app to a
platform without chaos.

## IaC principles
- **Declarative, not imperative** — describe the desired state; the tool
  reconciles. Re-running is safe (idempotent).
- **Version-controlled + reviewed** — infra changes go through PRs like code.
- **Plan before apply** — always review the diff (`terraform plan`) first.
- **Remote, locked state** — store state in GCS/S3/Azure Storage with locking so
  concurrent applies can't corrupt it. Never commit state (it holds secrets).
- **Modules** — factor common patterns (a "governed service") into reusable
  modules; environments just pass different variables.

## Policy as code
- Encode rules as code so they're testable and enforced automatically.
- **Shift left**: run policy checks in CI (Conftest/OPA) against the plan.
- **Enforce at the platform**: GCP Org Policy / Azure Policy / AWS SCP stop
  violations even if CI is bypassed.
- Examples: required labels, approved regions, no public ingress on prod, no
  service-account keys, encryption required.

## Identity governance
- Least privilege: grant the narrowest role at the smallest scope.
- Prefer keyless auth (OIDC / Workload Identity Federation) over static keys.
- Separate humans (SSO groups) from workloads (service accounts).
- Review access regularly; remove unused grants.

## Tagging / labeling standard
Minimum every resource should carry: `team`, `cost_center`, `owner`,
`environment`. This powers:
- **Cost attribution** — who spent what (showback/chargeback).
- **Ownership** — who to contact when something breaks.
- **Automation** — policies and cleanup jobs key off tags.

## Cost governance (FinOps)
- Budgets + alerts per project/environment.
- Quotas to cap blast radius.
- Rightsizing + scale-to-zero for non-prod (ties to Module 7).
- Regular cost reviews with the tags above.

## Drift detection
Out-of-band console changes cause "drift" from your code. Run a scheduled
`terraform plan` (read-only) in CI; a non-empty diff means someone changed infra
manually — investigate and reconcile.

## Compliance
Map controls to a framework (CIS, SOC 2, ISO 27001, HIPAA). IaC + policy-as-code
give you **evidence**: every change is reviewed, logged, and conformant by
construction. Continuous scanners (Trivy, Cloud Custodian, provider security
centers) catch regressions.

## Common pitfalls
- Click-ops changes that bypass code (causes drift).
- Committing state files or secrets.
- Over-broad IAM roles ("Owner"/"Contributor" everywhere).
- Untagged resources → no cost accountability.
- Policies only in CI (bypassable) and not at the platform.
