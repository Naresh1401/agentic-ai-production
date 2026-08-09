output "service_url" {
  description = "Public HTTPS URL of the deployed service."
  value       = google_cloud_run_v2_service.app.uri
}

output "runtime_service_account" {
  description = "Email of the least-privilege runtime service account."
  value       = google_service_account.run.email
}

output "labels" {
  description = "Effective governance labels applied to resources."
  value       = local.common_labels
}
