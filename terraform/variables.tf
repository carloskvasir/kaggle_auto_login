variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "GCP Region"
  type        = string
  default     = "us-central1"
}

variable "kaggle_email" {
  description = "Kaggle email for login"
  type        = string
  sensitive   = true
}

variable "kaggle_password" {
  description = "Kaggle password for login"
  type        = string
  sensitive   = true
}
