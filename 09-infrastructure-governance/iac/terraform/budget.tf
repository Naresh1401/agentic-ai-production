# Cost governance: a monthly budget with alert thresholds.
# Optional (enable_budget = true) because it requires a billing account id.
resource "google_billing_budget" "budget" {
  count = var.enable_budget ? 1 : 0

  billing_account = var.billing_account
  display_name    = "${var.service_name}-${var.environment}"

  budget_filter {
    projects = ["projects/${var.project_id}"]
  }

  amount {
    specified_amount {
      currency_code = "USD"
      units         = tostring(var.monthly_budget_usd)
    }
  }

  threshold_rules {
    threshold_percent = 0.5
  }
  threshold_rules {
    threshold_percent = 0.9
  }
  threshold_rules {
    threshold_percent = 1.0
  }
}
