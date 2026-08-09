variable "project_id" {
  type        = string
  description = "GCP project ID for this environment."
}

variable "region" {
  type        = string
  description = "Deployment region."
  default     = "us-central1"

  validation {
    # Governance: restrict to an approved region list.
    condition     = contains(["us-central1", "us-east1", "europe-west1"], var.region)
    error_message = "region must be one of the approved regions."
  }
}

variable "service_name" {
  type        = string
  description = "Cloud Run service name."
  default     = "agentic-ai"
}

variable "image" {
  type        = string
  description = "Fully-qualified container image (Artifact Registry)."
}

variable "environment" {
  type        = string
  description = "Deployment environment."

  validation {
    condition     = contains(["dev", "stage", "prod"], var.environment)
    error_message = "environment must be one of: dev, stage, prod."
  }
}

variable "openai_secret_id" {
  type        = string
  description = "Secret Manager secret id holding the OpenAI API key."
  default     = "openai-key"
}

variable "min_instances" {
  type        = number
  description = "Minimum Cloud Run instances."
  default     = 0
}

variable "max_instances" {
  type        = number
  description = "Maximum Cloud Run instances."
  default     = 3
}

variable "labels" {
  type        = map(string)
  description = "Governance labels. team, cost_center, and owner are required."

  validation {
    condition     = alltrue([for k in ["team", "cost_center", "owner"] : contains(keys(var.labels), k)])
    error_message = "labels must include team, cost_center, and owner."
  }
}

variable "enable_budget" {
  type        = bool
  description = "Create a billing budget with alert thresholds."
  default     = false
}

variable "billing_account" {
  type        = string
  description = "Billing account id (required when enable_budget = true)."
  default     = ""
}

variable "monthly_budget_usd" {
  type        = number
  description = "Monthly budget amount in USD."
  default     = 100
}

