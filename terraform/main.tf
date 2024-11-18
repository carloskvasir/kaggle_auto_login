terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# Cloud Storage para o código fonte
resource "google_storage_bucket" "function_bucket" {
  name     = "${var.project_id}-kaggle-login-source"
  location = var.region
  versioning {
    enabled = true
  }
}

# ZIP do código fonte
data "archive_file" "source" {
  type        = "zip"
  source_dir  = "${path.module}/src"
  output_path = "${path.module}/function-source.zip"
}

# Upload do código
resource "google_storage_bucket_object" "zip" {
  name   = "function-source-${data.archive_file.source.output_md5}.zip"
  bucket = google_storage_bucket.function_bucket.name
  source = data.archive_file.source.output_path
}

# Secret Manager para credenciais
resource "google_secret_manager_secret" "kaggle_email" {
  secret_id = "kaggle-email"
  
  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret" "kaggle_password" {
  secret_id = "kaggle-password"
  
  replication {
    automatic = true
  }
}

# Cloud Function
resource "google_cloudfunctions2_function" "kaggle_login" {
  name        = "kaggle-login"
  location    = var.region
  description = "Automated Kaggle login function"

  build_config {
    runtime     = "python39"
    entry_point = "kaggle_login"
    source {
      storage_source {
        bucket = google_storage_bucket.function_bucket.name
        object = google_storage_bucket_object.zip.name
      }
    }
  }

  service_config {
    max_instance_count = 1
    available_memory   = "128Mi"
    timeout_seconds    = 60
    
    secret_environment_variables {
      key        = "KAGGLE_EMAIL"
      secret     = google_secret_manager_secret.kaggle_email.secret_id
      version    = "latest"
      project_id = var.project_id
    }
    
    secret_environment_variables {
      key        = "KAGGLE_PASSWORD"
      secret     = google_secret_manager_secret.kaggle_password.secret_id
      version    = "latest"
      project_id = var.project_id
    }
  }
}

# Service Account
resource "google_service_account" "function_invoker" {
  account_id   = "kaggle-function-invoker"
  display_name = "Kaggle Function Invoker"
}

# Cloud Scheduler
resource "google_cloud_scheduler_job" "kaggle_login_job" {
  name        = "kaggle-daily-login"
  description = "Triggers Kaggle login function daily"
  schedule    = "0 12 * * *"
  time_zone   = "America/Sao_Paulo"

  http_target {
    http_method = "POST"
    uri         = google_cloudfunctions2_function.kaggle_login.url
    
    oidc_token {
      service_account_email = google_service_account.function_invoker.email
    }
  }
}

# IAM
resource "google_cloudfunctions2_function_iam_member" "invoker" {
  project        = google_cloudfunctions2_function.kaggle_login.project
  location       = google_cloudfunctions2_function.kaggle_login.location
  cloud_function = google_cloudfunctions2_function.kaggle_login.name
  role           = "roles/cloudfunctions.invoker"
  member         = "serviceAccount:${google_service_account.function_invoker.email}"
}
