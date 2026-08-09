project_id    = "agentic-prod"
region        = "us-central1"
service_name  = "agentic-ai"
image         = "us-central1-docker.pkg.dev/agentic-shared/agentic/agentic-ai:latest"
environment   = "prod"
min_instances = 2
max_instances = 20

# Cost governance on prod
enable_budget      = true
billing_account    = "000000-000000-000000"
monthly_budget_usd = 500

labels = {
  team        = "ai-platform"
  cost_center = "1234"
  owner       = "naresh"
}
