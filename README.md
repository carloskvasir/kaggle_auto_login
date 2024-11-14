# Kaggle Auto Login 🤖
![Daily Login Streak Badge](https://raw.githubusercontent.com/carloskvasir/kaggle_auto_login/main/image.png)
<img alt="Python Version" src="https://img.shields.io/badge/python-3.6+-blue">
[![License: MPL 2.0](https://img.shields.io/badge/License-MPL_2.0-brightgreen.svg)](https://opensource.org/licenses/MPL-2.0)

## 🎯 Overview
Automated authentication tool designed to maintain daily login streaks on Kaggle platform, helping users earn consistency badges through scheduled logins.

## ✨ Features
 - 🔐 Automated Kaggle authentication
 - 🔒 Secure environment variables management
 - 🛡️ XSRF token handling
 - 📡 HTTP session management
 - 🎯 Custom headers support

## 📋 Requirements
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
cp .env.example .env
```

## ⚙️ Configuration
Edit your .env file:
```bash
EMAIL=your_kaggle_email
PASSWORD=your_kaggle_password
USER=your_kaggle_username
```

## 📖 Usage
```bash
# Basic usage
python login.py

# As a cron job (recommended)
0 12 * * * /usr/bin/python3 /path/to/login.py
```

## 🛠️ Development
Tech Stack
 - Python 3.6+
 - requests
 - beautifulsoup4
 - python-dotenv

## 📜 License

This project is licensed under the Mozilla Public License Version 2.0 - see the [LICENSE](LICENSE) file for details.

## 👤 Author
Carlos Kvasir Lima

GitHub: @carloskvasir