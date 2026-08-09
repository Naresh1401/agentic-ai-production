# Unit tests for the governance policy. Run: opa test policy -v
package main_test

import data.main
import rego.v1

# A plan that violates two rules: missing labels + non-approved region.
non_compliant := {"resource_changes": [{
	"address": "google_cloud_run_v2_service.app",
	"type": "google_cloud_run_v2_service",
	"change": {"after": {
		"location": "asia-south1",
		"labels": {"team": "ai"},
	}},
}]}

# A fully governed plan: all labels present, approved region.
compliant := {"resource_changes": [{
	"address": "google_cloud_run_v2_service.app",
	"type": "google_cloud_run_v2_service",
	"change": {"after": {
		"location": "us-central1",
		"labels": {"team": "ai", "cost_center": "1234", "owner": "naresh", "environment": "dev"},
	}},
}]}

test_denies_missing_labels_and_bad_region if {
	count(main.deny) == 2 with input as non_compliant
}

test_allows_compliant_plan if {
	count(main.deny) == 0 with input as compliant
}
