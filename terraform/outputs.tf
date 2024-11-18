output "function_url" {
  description = "URL of the deployed Cloud Function"
  value       = google_cloudfunctions2_function.kaggle_login.url
}

output "function_status" {
  description = "Status of the Cloud Function"
  value       = google_cloudfunctions2_function.kaggle_login.state
}

output "scheduler_job" {
  description = "Name of the Cloud Scheduler job"
  value       = google_cloud_scheduler_job.kaggle_login_job.name
}
