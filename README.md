# Kaggle Auto Login 🤖
[![Python Version](https://img.shields.io/badge/python-3.6+-blue)](https://www.python.org/)
[![License: MPL 2.0](https://img.shields.io/badge/License-MPL_2.0-brightgreen.svg)](https://opensource.org/licenses/MPL-2.0)

## 🎯 Overview
Automated authentication tool designed to maintain daily login streaks on Kaggle platform, helping users earn consistency badges through scheduled logins.

## ✨ Features
 - 🔐 Automated Kaggle authentication
 - 🌩️ Secure environment variables management
 - 🔒 XSRF token handling
 - 📊 HTTP session management
 - 📈 Custom headers support

## 🛠️ Requirements
 - Python 3.6+
 - pip

## 🚀 Quick Start
```bash
# Clone repository
git clone git@github.com:carloskvasir/kaggle_auto_login.git
cd kaggle-auto-login

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env{.example,}
```

## 📝 Configuration
Edit your .env file:
```bash
EMAIL=your_kaggle_email
PASSWORD=your_kaggle_password
USER=your_kaggle_username
```

## 📊 Usage
```bash
# Basic usage
python kaggle_auto_login.py

# As a cron job (recommended)
0 12 * * * /usr/bin/python3 /path/to/kaggle_auto_login.py
```

## 📈 Development
Tech Stack
 - Python 3.6+
 - requests
 - beautifulsoup4
 - python-dotenv

## 🌩️ Cloud Deployment (GCP)

### 🎯 Overview
The project can be deployed on Google Cloud Platform (GCP) using a serverless architecture that includes:
- ⚡ Cloud Functions for script execution
- ⏰ Cloud Scheduler for automatic scheduling
- 🔑 Secret Manager for secure credentials management
- 💾 Cloud Storage for source code storage

### 📝 Prerequisites
- GCP Account with billing enabled
- [Terraform](https://www.terraform.io/) installed (v1.0+)
- [Google Cloud CLI](https://cloud.google.com/sdk/docs/install) installed and configured
- GCP Project created

### 🚀 GCP Environment Setup

1. **GCP Authentication**:
   ```bash
   # Login to GCP
   gcloud auth login

   # Configure project
   gcloud config set project YOUR_PROJECT_ID
   ```

2. **Enable Required APIs**:
   ```bash
   # Enable necessary APIs
   gcloud services enable \
     cloudfunctions.googleapis.com \
     cloudscheduler.googleapis.com \
     secretmanager.googleapis.com \
     cloudbuild.googleapis.com
   ```

### 📈 Terraform Deployment

1. **Prepare Configuration**:
   ```bash
   # Navigate to terraform directory
   cd terraform/

   # Copy example variables file
   cp terraform.tfvars.example terraform.tfvars

   # Edit configuration file
   nano terraform.tfvars
   ```

2. **Configure Variables**:
   ```hcl
   # terraform.tfvars
   project_id      = "your-project-id"
   region          = "us-central1"
   kaggle_email    = "your-email@example.com"
   kaggle_password = "your-kaggle-password"
   ```

3. **Initialize and Apply Terraform**:
   ```bash
   # Initialize Terraform
   terraform init

   # Review execution plan
   terraform plan

   # Apply changes
   terraform apply
   ```

### 📊 Monitoring and Logs

1. **View Logs**:
   ```bash
   # Check Cloud Function logs
   gcloud functions logs read kaggle-login
   ```

2. **Monitor Executions**:
   - Access GCP Console > Cloud Functions
   - Check execution status
   - Configure alerts if needed

### 📊 Costs
The configuration uses GCP free tier components:
- Cloud Functions: 2 million free invocations/month
- Cloud Scheduler: 3 free jobs/month
- Secret Manager: 10,000 free accesses/month
- Cloud Storage: 5GB free storage/month

For this usage (1 execution/day), expected monthly cost is $0.00.

### 🔒 Security
- 🔐 Credentials managed via Secret Manager
- 👮 IAM with least privilege principle
- 🔒 HTTPS for all communications
- 🎯 Dedicated Service Account for Cloud Scheduler

### 🚨 Troubleshooting

1. **Permission Error**:
   ```bash
   # Check Service Account permissions
   gcloud projects get-iam-policy YOUR_PROJECT_ID
   ```

2. **Function Not Executing**:
   - Check function logs
   - Verify scheduler timezone
   - Validate Secret Manager credentials

### 🚮 Resource Cleanup
```bash
# Remove all infrastructure
terraform destroy
```

## 📜 License

This project is licensed under the Mozilla Public License Version 2.0 - see the [LICENSE](LICENSE) file for details.

## 👤 Author
Carlos Kvasir Lima
