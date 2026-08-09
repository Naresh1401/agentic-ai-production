terraform {
  required_version = ">= 1.5"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }

  # Governance: use a remote, locked backend in real projects (not local state).
  # backend "gcs" {
  #   bucket = "my-tf-state-bucket"
  #   prefix = "agentic-ai"
  # }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

locals {
  # Every resource carries a consistent, auditable set of labels.
  common_labels = merge(var.labels, {
    environment = var.environment
    managed_by  = "terraform"
  })
}

# Least-privilege runtime identity — no static keys anywhere.
resource "google_service_account" "run" {
  account_id   = "${var.service_name}-run"
  display_name = "Runtime service account for ${var.service_name}"
}

# Grant only the one permission the app needs: read the OpenAI key secret.
resource "google_secret_manager_secret_iam_member" "run_secret_access" {
  secret_id = var.openai_secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.run.email}"
}

resource "google_cloud_run_v2_service" "app" {
  name     = var.service_name
  location = var.region
  labels   = local.common_labels

  template {
    service_account = google_service_account.run.email

    scaling {
      min_instance_count = var.min_instances
      max_instance_count = var.max_instances
    }

    containers {
      image = var.image

      env {
        name  = "APP_ENV"
        value = var.environment
      }

      env {
        name = "OPENAI_API_KEY"
        value_source {
          secret_key_ref {
            secret  = var.openai_secret_id
            version = "latest"
          }
        }
      }
    }
  }
}
