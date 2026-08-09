# Module 5 — Cloud (AWS / GCP / Azure)

**Goal:** run your containerized agent on a managed cloud runtime, safely
configured, across **dev / stage / prod / on-prem**.

## In this module
- **[environments/](environments/)** — dev / stage / prod / on-prem strategy,
  per-environment config, and the promotion flow. **Read this first.**
- **[azure/](azure/README.md)** — Azure from scratch, in depth.
- **[gcp/](gcp/README.md)** — Google Cloud from scratch, in depth.
- This README — the quick, cross-cloud overview below.

## Pick a runtime
| Cloud | Easiest agent runtime | Serverless? | Notes |
|-------|----------------------|-------------|-------|
| **GCP** | Cloud Run | ✅ scale-to-zero | Simplest for containers; great default |
| **AWS** | ECS Fargate / App Runner | App Runner ✅ | Lambda works for short, non-streaming |
| **Azure** | Container Apps | ✅ scale-to-zero | KEDA autoscaling, Dapr optional |

> Recommendation: learn **Cloud Run** first (fastest path), then map the same
> ideas to ECS/Container Apps.

## Deploy the container (Module 6 builds it)

### GCP Cloud Run
```bash
gcloud run deploy agentic-ai \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-secrets OPENAI_API_KEY=openai-key:latest
```

### AWS App Runner (from a pushed image)
```bash
aws ecr create-repository --repository-name agentic-ai
# build/push image (see Module 6), then create an App Runner service
# pointing at the ECR image; set env/secrets in the service config.
```

### Azure Container Apps
```bash
az containerapp up \
  --name agentic-ai \
  --resource-group rg-agentic \
  --ingress external --target-port 8000 \
  --source .
```

## Cloud fundamentals to learn
- **Identity** — IAM roles / service accounts / managed identities (no static keys)
- **Secrets** — Secret Manager / AWS Secrets Manager / Key Vault
- **Networking** — ingress, egress, VPC/private endpoints, TLS
- **Autoscaling** — min/max instances, concurrency per instance, scale-to-zero
- **Config per env** — dev/stage/prod via env vars, not code
- **Cost controls** — budgets + alerts

## Security must-dos
- No long-lived keys in images or code — use the platform secret store.
- Least-privilege IAM: only the permissions the service needs.
- Private egress + allowlist for outbound LLM/tool calls where possible.

## Exercises
1. Deploy the container to one cloud; hit `/health` over HTTPS.
2. Store the API key in the cloud secret manager, inject at runtime.
3. Configure autoscaling (min 0, max N) and load-test it.
4. Add a budget alert.
5. Stand up the **same app in dev, stage, and prod** using the configs in
   [environments/](environments/), promoting one image across all three.

## 📚 References
- GCP Cloud Run: https://cloud.google.com/run/docs
- AWS ECS / Fargate: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/Welcome.html
- AWS App Runner: https://docs.aws.amazon.com/apprunner/
- Azure Container Apps: https://learn.microsoft.com/en-us/azure/container-apps/
- GCP Workload Identity Federation: https://cloud.google.com/iam/docs/workload-identity-federation
- Well-Architected: [AWS](https://aws.amazon.com/architecture/well-architected/) · [Azure](https://learn.microsoft.com/en-us/azure/well-architected/) · [GCP](https://cloud.google.com/architecture/framework)

## Definition of done
- [ ] Public HTTPS URL serving `/chat`
- [ ] Secrets injected from a secret manager (not baked in)
- [ ] Autoscaling configured
- [ ] A cost budget + alert exists
- [x] dev / stage / prod defined with separate secrets + config
- [x] On-prem deployment path documented (see [environments/](environments/))
