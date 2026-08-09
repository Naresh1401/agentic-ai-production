# Azure — From Scratch, In Depth

A ground-up guide to running the agent service on Microsoft Azure across
**dev / stage / prod / on-prem**. No prior Azure knowledge assumed.

---

## 1. The mental model

Azure organizes everything in a hierarchy. Learn this first — it explains
billing, permissions, and isolation.

```
Tenant (your whole org / Entra ID directory)
└── Management Group           # optional, groups subscriptions
    └── Subscription           # billing + isolation boundary
        └── Resource Group      # a folder for related resources (one per env)
            └── Resources        # Container App, Key Vault, ACR, etc.
```

- **Tenant** = your identity directory (Microsoft Entra ID, formerly Azure AD).
- **Subscription** = where costs accrue and access is scoped. Many teams use a
  separate subscription per environment (prod vs non-prod) for hard isolation.
- **Resource Group (RG)** = a folder. Delete the RG → delete everything in it.
  Use **one RG per environment**: `rg-agentic-dev`, `-stage`, `-prod`.
- **Region** = physical datacenter location (e.g. `eastus`). Keep resources in
  the same region to reduce latency and egress cost.

---

## 2. One-time setup

### Create an account
1. Go to `azure.microsoft.com` → start free (gives credits).
2. This creates a **tenant** + a **subscription** automatically.

### Install the CLI and log in
```bash
# macOS
brew install azure-cli

az login                       # opens browser
az account show                # confirm the active subscription
az account list -o table       # list all subscriptions
az account set --subscription "<SUBSCRIPTION_ID>"
```

### Install the Container Apps extension (used below)
```bash
az extension add --name containerapp --upgrade
az provider register --namespace Microsoft.App
az provider register --namespace Microsoft.OperationalInsights
```

---

## 3. Core services you'll use (and why)

| Need | Azure service | Notes |
|------|---------------|-------|
| Run the container | **Azure Container Apps (ACA)** | Serverless, scale-to-zero, HTTPS, revisions. Best default for our API. |
| Store the image | **Azure Container Registry (ACR)** | Private Docker registry. |
| Store secrets | **Azure Key Vault** | API keys, DB passwords. Never bake into images. |
| Identity without keys | **Managed Identity** (Entra ID) | The app proves who it is with no stored credential. |
| Logs & traces | **Log Analytics** + **Application Insights** | Query logs (KQL), distributed tracing. |
| Metrics/alerts/budgets | **Azure Monitor** + **Cost Management** | SLO alerts, spend alerts. |
| LLM (optional) | **Azure OpenAI** / **Azure AI Foundry** | Managed models inside your tenant. |
| Networking/edge | **VNet**, **Private Endpoints**, **Front Door/App Gateway (WAF)** | Private egress + a public edge with a firewall. |

> Alternatives: **AKS** (managed Kubernetes) when you need full control or a
> lift-and-shift of an existing k8s setup — heavier than ACA. **App Service**
> for simple web apps. We use **ACA** as the primary path.

---

## 4. Deploy step by step (start with dev)

### 4.1 Create the resource group
```bash
az group create --name rg-agentic-dev --location eastus
```

### 4.2 Create a container registry and push the image
```bash
az acr create --resource-group rg-agentic-dev \
  --name acragenticdev --sku Basic          # name must be globally unique

az acr login --name acragenticdev

# Build from the repo root using our Module 6 Dockerfile
docker build -t acragenticdev.azurecr.io/agentic-ai:$(git rev-parse --short HEAD) \
  -f 06-docker-cicd/Dockerfile .
docker push acragenticdev.azurecr.io/agentic-ai:$(git rev-parse --short HEAD)
```

### 4.3 Store the secret in Key Vault
```bash
az keyvault create --name kv-agentic-dev --resource-group rg-agentic-dev --location eastus
az keyvault secret set --vault-name kv-agentic-dev --name openai-key --value "<YOUR_KEY>"
```

### 4.4 Create the Container Apps environment (shared runtime)
```bash
az containerapp env create \
  --name cae-agentic-dev \
  --resource-group rg-agentic-dev \
  --location eastus
```

### 4.5 Deploy the app with a managed identity + Key Vault secret
```bash
az containerapp create \
  --name agentic-ai \
  --resource-group rg-agentic-dev \
  --environment cae-agentic-dev \
  --image acragenticdev.azurecr.io/agentic-ai:$(git rev-parse --short HEAD) \
  --target-port 8000 \
  --ingress external \
  --system-assigned \
  --min-replicas 0 --max-replicas 1 \
  --env-vars APP_ENV=dev \
             OPENAI_API_KEY=secretref:openai-key \
  --secrets openai-key=keyvaultref:https://kv-agentic-dev.vault.azure.net/secrets/openai-key,identityref:system

# Get the public URL
az containerapp show -n agentic-ai -g rg-agentic-dev \
  --query properties.configuration.ingress.fqdn -o tsv
```

Test:
```bash
curl https://<fqdn>/health
```

> **Why managed identity?** The app authenticates to Key Vault/ACR using its
> Azure identity — there are **no passwords or keys stored anywhere**. Grant it
> access with a role assignment (`Key Vault Secrets User`).

---

## 5. Per-environment layout

Repeat the pattern with a separate RG (and ideally a separate subscription for
prod). Everything differs only by config — see
[../environments/README.md](../environments/README.md).

| Resource | dev | stage | prod |
|----------|-----|-------|------|
| Resource group | `rg-agentic-dev` | `rg-agentic-stage` | `rg-agentic-prod` |
| Registry | shared `acragentic` (or per-env) | | |
| Key Vault | `kv-agentic-dev` | `kv-agentic-stage` | `kv-agentic-prod` |
| Container App min replicas | 0 | 1 | 2 |
| Ingress | external (locked) | restricted | external + Front Door WAF |
| `APP_ENV` | dev | stage | prod |

Promote the **same image tag** across environments; only swap the RG, Key Vault
reference, and `APP_ENV`.

---

## 6. On-prem with Azure (hybrid)

For datacenter/air-gapped needs, Azure offers two bridges:

- **Azure Arc** — project on-prem Kubernetes/servers into Azure so you manage
  and govern them with the same tools (policies, monitoring) while workloads run
  locally.
- **Azure Stack (Hub/HCI)** — run Azure services on hardware in your own
  datacenter for data-residency/disconnected scenarios.

Typical on-prem stack for this app: your own **Kubernetes** cluster running the
container, a **self-hosted model** (vLLM/Ollama), **HashiCorp Vault** or k8s
secrets, and a local **OpenTelemetry** collector. Manage it centrally via Arc.

---

## 7. Identity, security, networking (the important part)

- **Microsoft Entra ID** is the identity backbone. Prefer **managed identities**
  and **role assignments (RBAC)** over connection strings/keys.
- **Least privilege**: assign the narrowest role (e.g. `Key Vault Secrets User`,
  not `Contributor`) to the app's identity.
- **Private networking**: put resources in a **VNet**, use **Private Endpoints**
  so traffic to Key Vault/ACR/OpenAI never touches the public internet.
- **Edge protection**: front prod with **Azure Front Door** or **Application
  Gateway** (both offer a **WAF**).
- **Secrets**: only in **Key Vault**, referenced at runtime. Rotate without
  redeploying.

---

## 8. Observability & cost

- **Application Insights** for distributed tracing (wire the OpenTelemetry SDK
  from Module 4 to the App Insights connection string).
- **Log Analytics** to query logs with **KQL**.
- **Azure Monitor alerts** on latency/error SLOs.
- **Cost Management + Budgets**: set a monthly budget with email alerts per RG.

```bash
# example: create a budget alert (portal is easier; CLI shown for reference)
az consumption budget create --budget-name agentic-prod-budget \
  --amount 200 --time-grain Monthly --category Cost \
  --resource-group rg-agentic-prod   # (exact flags vary by API version)
```

---

## 9. Infrastructure as Code (do this once you're comfortable)

Stop clicking/typing commands per environment — declare infra in code:

- **Bicep** (Azure-native, recommended) or **Terraform** (multi-cloud).
- Store templates in the repo; CI deploys them per environment.
- Benefit: dev/stage/prod are provably identical, reviewable, and repeatable.

Minimal Bicep sketch (`main.bicep`):
```bicep
param location string = resourceGroup().location
param appEnv string
resource acaEnv 'Microsoft.App/managedEnvironments@2024-03-01' = {
  name: 'cae-agentic-${appEnv}'
  location: location
}
// ... container app, key vault, registry references ...
```

---

## 10. Clean up (avoid surprise bills)
```bash
az group delete --name rg-agentic-dev --yes --no-wait
```

## Learning checklist
- [ ] Understand tenant → subscription → RG → resource
- [ ] Deploy the container to ACA in dev over HTTPS
- [ ] Pull the API key from Key Vault via managed identity (no stored keys)
- [ ] Wire tracing to Application Insights
- [ ] Set a budget alert
- [ ] Recreate the same app in stage + prod with only config changes
- [ ] Read up on Arc/Stack for the on-prem story
