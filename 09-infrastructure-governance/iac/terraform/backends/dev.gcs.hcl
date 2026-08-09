# Remote, locked Terraform state per environment.
# Usage: tofu init -backend-config=backends/dev.gcs.hcl
#
# Copy per environment (dev/stage/prod) with a distinct prefix. The GCS bucket
# provides state locking automatically. NEVER keep state locally in a team.
bucket = "agentic-tfstate-dev"
prefix = "agentic-ai/dev"
