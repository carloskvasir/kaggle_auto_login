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

# Source code storage and packaging
resource "google_storage_bucket" "source" {
  name     = "${var.project_id}-kaggle-login"
  location = var.region
  versioning {
    enabled = true
  }
}

data "archive_file" "source" {
  type        = "zip"
  source_dir  = "${path.root}/.."
  output_path = "${path.module}/function-source.zip"
  excludes    = ["venv", ".git", ".env", "terraform", "*.log", "*.png", "LICENSE"]
}

resource "google_storage_bucket_object" "source" {
  name   = "source-${data.archive_file.source.output_md5}.zip"
  bucket = google_storage_bucket.source.name
  source = data.archive_file.source.output_path
}

# Secrets management
resource "google_secret_manager_secret" "kaggle_email" {
  secret_id = "kaggle-email"
  
  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_version" "kaggle_email" {
  secret      = google_secret_manager_secret.kaggle_email.id
  secret_data = var.kaggle_email
}

resource "google_secret_manager_secret" "kaggle_password" {
  secret_id = "kaggle-password"
  
  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_version" "kaggle_password" {
  secret      = google_secret_manager_secret.kaggle_password.id
  secret_data = var.kaggle_password
}

# Cloud Function
resource "google_cloudfunctions2_function" "login" {
  name        = "kaggle-login"
  location    = var.region
  description = "Automated Kaggle login function"

  build_config {
    runtime     = "python39"
    entry_point = "main"  
    source {
      storage_source {
        bucket = google_storage_bucket.source.name
        object = google_storage_bucket_object.source.name
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

# Scheduler configuration
resource "google_service_account" "scheduler" {
  account_id   = "kaggle-scheduler"
  display_name = "Kaggle Login Scheduler"
}

resource "google_cloud_scheduler_job" "daily_login" {
  name        = "kaggle-daily-login"
  description = "Triggers Kaggle login function daily"
  schedule    = "0 12 * * *"  
  time_zone   = "America/Sao_Paulo"

  http_target {
    http_method = "POST"
    uri         = google_cloudfunctions2_function.login.url
    
    oidc_token {
      service_account_email = google_service_account.scheduler.email
    }
  }
}

# IAM permissions
resource "google_cloudfunctions2_function_iam_member" "invoker" {
  project        = google_cloudfunctions2_function.login.project
  location       = google_cloudfunctions2_function.login.location
  cloud_function = google_cloudfunctions2_function.login.name
  role           = "roles/cloudfunctions.invoker"
  member         = "serviceAccount:${google_service_account.scheduler.email}"
}
