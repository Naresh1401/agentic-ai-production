# Google Cloud (GCP) — From Scratch, In Depth

A ground-up guide to running the agent service on Google Cloud across
**dev / stage / prod / on-prem**. No prior GCP knowledge assumed.

---

## 1. The mental model

GCP's hierarchy controls billing, permissions (IAM), and isolation. Learn it
first.

```
Organization (your company domain, optional)
└── Folder                 # optional grouping (e.g. by team/env)
    └── Project             # the core unit: isolation + billing + APIs
        └── Resources        # Cloud Run service, secrets, registry, etc.
```

- **Project** = the fundamental boundary. Resources, APIs, IAM, and billing all
  attach to a project. Use **one project per environment**:
  `agentic-dev`, `agentic-stage`, `agentic-prod`.
- **Billing account** = where charges go; linked to projects.
- **Region/zone** = physical location (e.g. `us-central1`). Keep resources
  co-located to cut latency and egress cost.
- **APIs** must be **enabled per project** before use (e.g. Cloud Run API).

> GCP tip: separate projects give the cleanest isolation. Deleting a project
> deletes everything in it — great for tearing down experiments.

---

## 2. One-time setup

### Create an account & project
1. Go to `cloud.google.com` → get started (free credits).
2. Create a project (console or CLI below).

### Install the CLI and log in
```bash
# macOS
brew install --cask google-cloud-sdk

gcloud auth login                       # opens browser
gcloud auth application-default login   # for local SDKs/libraries

# Create and select a project
gcloud projects create agentic-dev --name="Agentic Dev"
gcloud config set project agentic-dev
gcloud config set run/region us-central1
```

### Link billing & enable the APIs you need
```bash
gcloud billing accounts list
gcloud billing projects link agentic-dev --billing-account=<BILLING_ACCOUNT_ID>

gcloud services enable \
  run.googleapis.com \
  artifactregistry.googleapis.com \
  secretmanager.googleapis.com \
  cloudbuild.googleapis.com \
  logging.googleapis.com \
  cloudtrace.googleapis.com \
  aiplatform.googleapis.com
```

---

## 3. Core services you'll use (and why)

| Need | GCP service | Notes |
|------|-------------|-------|
| Run the container | **Cloud Run** | Serverless, scale-to-zero, HTTPS, revisions. Best default for our API. |
| Store the image | **Artifact Registry** | Private Docker registry (replaces old GCR). |
| Store secrets | **Secret Manager** | API keys, DB passwords. Versioned. |
| Identity without keys | **Service Accounts** + **Workload Identity** | The app authenticates as a service account, no key files. |
| Logs | **Cloud Logging** | Central logs, powerful filters. |
| Traces | **Cloud Trace** | Distributed tracing (wire OTEL from Module 4). |
| Metrics/alerts | **Cloud Monitoring** | SLOs, alerting policies. |
| Budgets | **Cloud Billing budgets** | Spend alerts. |
| LLM (optional) | **Vertex AI** | Managed models (Gemini + others) in your project. |
| Networking/edge | **VPC**, **Serverless VPC Connector**, **Cloud Load Balancing + Cloud Armor (WAF)** | Private egress + protected public edge. |

> Alternatives: **GKE** (managed Kubernetes) for full control or existing k8s
> workloads — heavier than Cloud Run. **Cloud Functions** for tiny event
> handlers. We use **Cloud Run** as the primary path.

---

## 4. Deploy step by step (start with dev)

### 4.1 Create an Artifact Registry repo & push the image
```bash
gcloud artifacts repositories create agentic \
  --repository-format=docker --location=us-central1

# Auth docker to the registry
gcloud auth configure-docker us-central1-docker.pkg.dev

TAG=us-central1-docker.pkg.dev/agentic-dev/agentic/agentic-ai:$(git rev-parse --short HEAD)
docker build -t "$TAG" -f 06-docker-cicd/Dockerfile .
docker push "$TAG"
```

### 4.2 Store the secret in Secret Manager
```bash
printf '%s' "<YOUR_OPENAI_KEY>" | \
  gcloud secrets create openai-key --data-file=-
# later updates: gcloud secrets versions add openai-key --data-file=-
```

### 4.3 Create a least-privilege service account
```bash
gcloud iam service-accounts create agentic-run \
  --display-name="Agentic Cloud Run"

# Allow it to read only the one secret it needs
gcloud secrets add-iam-policy-binding openai-key \
  --member="serviceAccount:agentic-run@agentic-dev.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

### 4.4 Deploy to Cloud Run (secret injected as env var)
```bash
gcloud run deploy agentic-ai \
  --image "$TAG" \
  --service-account agentic-run@agentic-dev.iam.gserviceaccount.com \
  --set-env-vars APP_ENV=dev \
  --set-secrets OPENAI_API_KEY=openai-key:latest \
  --min-instances 0 --max-instances 1 \
  --concurrency 20 \
  --allow-unauthenticated      # dev only; lock down for stage/prod

# The command prints the HTTPS URL. Test it:
curl https://<service-url>/health
```

> Cloud Run injects a `PORT` env var; our Dockerfile already binds to it. Cloud
> Run handles TLS, autoscaling, and zero-downtime revisions for you.

---

## 5. Per-environment layout

Use a separate **project** per environment. Config is the only difference — see
[../environments/README.md](../environments/README.md).

| Item | dev | stage | prod |
|------|-----|-------|------|
| Project | `agentic-dev` | `agentic-stage` | `agentic-prod` |
| Min instances | 0 | 1 | 2 |
| Max instances | 1 | 3 | autoscale |
| Access | `--allow-unauthenticated` | IAM/IAP restricted | public + Cloud Armor |
| `APP_ENV` | dev | stage | prod |

Promote the **same image digest** across projects; change only the project,
secret binding, and `APP_ENV`.

---

## 6. On-prem with GCP (hybrid)

For datacenter/air-gapped needs, GCP offers:

- **Anthos / GKE on-prem (Google Distributed Cloud)** — run GKE-managed
  Kubernetes inside your own datacenter, managed centrally from GCP.
- **Connect gateway + Config Management** — govern on-prem clusters with the
  same policies as cloud.

Typical on-prem stack for this app: your **Kubernetes** cluster running the
container, a **self-hosted model** (vLLM/Ollama/TGI), **Vault** or k8s secrets,
and a local **OpenTelemetry** collector. Manage centrally via Anthos.

---

## 7. Identity, security, networking (the important part)

- **IAM** is everything in GCP: *who* (member) can do *what* (role) on *which*
  resource. Grant **predefined roles** at the narrowest scope.
- **Service accounts** are machine identities. Prefer **Workload Identity** over
  downloading JSON key files (key files leak and are hard to rotate).
- **Least privilege**: the run service account should only have
  `secretmanager.secretAccessor` on the specific secret, not project-wide roles.
- **Private networking**: use a **VPC** + **Serverless VPC Connector** so Cloud
  Run egress goes through your network; use **Private Google Access** and
  **VPC Service Controls** to prevent data exfiltration.
- **Edge protection**: front prod with an **HTTPS Load Balancer + Cloud Armor**
  (WAF, rate limiting, geo rules). Require auth via **IAP** for internal apps.
- **Secrets**: only in **Secret Manager**, referenced at deploy time.

---

## 8. Observability & cost

- **Cloud Trace** for distributed traces — point the OpenTelemetry exporter from
  Module 4 at Cloud Trace (or an OTLP collector).
- **Cloud Logging** with structured JSON logs and a `request_id`.
- **Cloud Monitoring** alerting policies on latency/error SLOs.
- **Billing budgets**:
```bash
gcloud billing budgets create \
  --billing-account=<BILLING_ACCOUNT_ID> \
  --display-name="agentic-prod-budget" \
  --budget-amount=200USD \
  --filter-projects=projects/agentic-prod
```

---

## 9. Infrastructure as Code (do this once you're comfortable)

Declare infra in code instead of running commands per environment:

- **Terraform** (recommended, multi-cloud) or **Config Connector** (k8s-style).
- Keep `.tf` files in the repo; CI applies them per project/environment.
- Benefit: dev/stage/prod are provably identical and reviewable.

Minimal Terraform sketch:
```hcl
resource "google_cloud_run_v2_service" "agentic" {
  name     = "agentic-ai"
  location = "us-central1"
  template {
    service_account = google_service_account.agentic_run.email
    containers {
      image = var.image
      env { name = "APP_ENV" value = var.app_env }
    }
    scaling { min_instance_count = var.min_instances }
  }
}
```

---

## 10. Clean up (avoid surprise bills)
```bash
gcloud run services delete agentic-ai --region us-central1
# or nuke everything:
gcloud projects delete agentic-dev
```

## Learning checklist
- [ ] Understand org → folder → project → resource + per-project APIs
- [ ] Deploy the container to Cloud Run in dev over HTTPS
- [ ] Pull the API key from Secret Manager via a least-privilege service account
- [ ] Wire tracing to Cloud Trace
- [ ] Set a billing budget
- [ ] Recreate the same service in stage + prod (separate projects) with only config changes
- [ ] Read up on Anthos / GKE on-prem for the on-prem story

---

## Azure ↔ GCP quick map (so the two guides reinforce each other)

| Concept | Azure | GCP |
|---------|-------|-----|
| Isolation/billing unit | Subscription + Resource Group | Project |
| Run a container (serverless) | Container Apps | Cloud Run |
| Image registry | Container Registry (ACR) | Artifact Registry |
| Secrets | Key Vault | Secret Manager |
| Machine identity | Managed Identity | Service Account / Workload Identity |
| Identity system | Microsoft Entra ID | Cloud IAM |
| Logs | Log Analytics | Cloud Logging |
| Traces | Application Insights | Cloud Trace |
| Metrics/alerts | Azure Monitor | Cloud Monitoring |
| Managed Kubernetes | AKS | GKE |
| WAF/edge | Front Door / App Gateway | Cloud Armor + HTTPS LB |
| On-prem/hybrid | Arc / Azure Stack | Anthos / GKE on-prem |
| Managed LLMs | Azure OpenAI / AI Foundry | Vertex AI |
| IaC (native) | Bicep | (Terraform / Config Connector) |
