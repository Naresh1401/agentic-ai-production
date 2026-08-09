# Policy-as-code: block Cloud Run services that are missing governance labels.
#
# Run against a Terraform plan converted to JSON:
#   terraform show -json plan.tfplan > plan.json
#   conftest test plan.json --policy 09-infrastructure-governance/policy
package main

# Labels every governed resource must carry.
required_labels := {"team", "cost_center", "owner", "environment"}

# Inspect planned Cloud Run services in the Terraform plan.
deny[msg] {
	rc := input.resource_changes[_]
	rc.type == "google_cloud_run_v2_service"
	labels := object.get(rc.change.after, "labels", {})
	provided := {k | labels[k]}
	missing := required_labels - provided
	count(missing) > 0
	msg := sprintf("Cloud Run '%s' is missing required labels: %v", [rc.address, missing])
}

# Governance: disallow deployment to non-approved regions.
approved_regions := {"us-central1", "us-east1", "europe-west1"}

deny[msg] {
	rc := input.resource_changes[_]
	rc.type == "google_cloud_run_v2_service"
	region := rc.change.after.location
	not approved_regions[region]
	msg := sprintf("Cloud Run '%s' uses non-approved region '%s'", [rc.address, region])
}
