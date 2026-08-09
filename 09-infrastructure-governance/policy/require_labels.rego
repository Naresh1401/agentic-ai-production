# Policy-as-code: block Cloud Run services that are missing governance labels.
#
# Run against a Terraform plan converted to JSON:
#   terraform show -json plan.tfplan > plan.json
#   conftest test plan.json --policy 09-infrastructure-governance/policy
package main

import rego.v1

# Labels every governed resource must carry.
required_labels := {"team", "cost_center", "owner", "environment"}

# Regions the org allows deployments into.
approved_regions := {"us-central1", "us-east1", "europe-west1"}

# Deny Cloud Run services missing any required governance label.
deny contains msg if {
	some rc in input.resource_changes
	rc.type == "google_cloud_run_v2_service"
	labels := object.get(rc.change.after, "labels", {})
	provided := {k | some k, _ in labels}
	missing := required_labels - provided
	count(missing) > 0
	msg := sprintf("Cloud Run '%s' is missing required labels: %v", [rc.address, missing])
}

# Deny deployment to non-approved regions.
deny contains msg if {
	some rc in input.resource_changes
	rc.type == "google_cloud_run_v2_service"
	region := rc.change.after.location
	not approved_regions[region]
	msg := sprintf("Cloud Run '%s' uses non-approved region '%s'", [rc.address, region])
}
