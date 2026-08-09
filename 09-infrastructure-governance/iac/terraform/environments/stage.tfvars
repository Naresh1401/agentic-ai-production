project_id    = "agentic-stage"
region        = "us-central1"
service_name  = "agentic-ai"
image         = "us-central1-docker.pkg.dev/agentic-shared/agentic/agentic-ai:latest"
environment   = "stage"
min_instances = 1
max_instances = 3

labels = {
  team        = "ai-platform"
  cost_center = "1234"
  owner       = "naresh"
}
