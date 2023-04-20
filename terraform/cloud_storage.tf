# resource "google_storage_bucket" "bucket"  {
#   project    = var.project_id
#   name   = var.bucket_name
#   location = "EUROPE-WEST4"
#   storage_class = "STANDARD"
#   force_destroy        = false
#   uniform_bucket_level_access = true
# }

# data "google_iam_policy" "admin" {
#   binding {
#     role = "roles/storage.objectAdmin"
#     members = [
#       google_service_account.cloud_function_service_account.name
#     ]
#   }
# }

# resource "google_storage_bucket_iam_policy" "policy" {
#   bucket = google_storage_bucket.bucket.name
#   policy_data = data.google_iam_policy.admin.policy_data
# }
