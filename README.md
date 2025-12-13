# 🔐 PKI-Based 2FA Microservice

A FastAPI microservice implementing **Public Key Infrastructure (PKI)**–secured  
**Two-Factor Authentication (2FA)** using encrypted TOTP seeds, RSA signatures,  
and container-ready deployment.


## ✨ Features
- RSA-based digital signature verification
- Encrypted TOTP seed handling (hybrid RSA + AES)
- Time-based One-Time Password (TOTP) authentication
- FastAPI RESTful API
- Docker-ready configuration with persistence support


## 🧰 Tech Stack
- Python 3.11
- FastAPI
- cryptography
- pyotp
- pytest
- Docker & Docker Compose


## 📁 Project Structure
app/
├── init.py
├── config.py
├── crypto_utils.py
├── totp_utils.py
└── main.py

scripts/
├── generate_keys.py
├── generate_seed.py
└── sign_file.py

tests/
├── test_crypto.py
└── test_endpoints.py

docker-compose.yml
Dockerfile
encrypted_seed.txt
encrypted_seed.sig
student_public.pem
instructor_public.pem
requirements.txt
README.md


## ⚙️ Prerequisites
- Python 3.11+
- Git
- Docker & Docker Compose (optional – see note below)

## 🚀 Local Setup (Without Docker)

### 1️⃣ Create and activate virtual environment

python -m venv .venv
source .venv/Scripts/activate    # Git Bash (Windows)

## 2️⃣ Install dependencies

pip install -r requirements.txt

## 🔑 Key & Seed Generation

python scripts/generate_keys.py
python scripts/generate_seed.py
python scripts/sign_file.py

This generates:

RSA key pairs
Encrypted TOTP seed
Encrypted seed signature

## ▶️ Run Application Locally

uvicorn app.main:app --host 0.0.0.0 --port 8000
Service available at:
http://localhost:8000

## 🔌 API Endpoints
Health Check:

-GET /health

Store Encrypted Seed:

-POST /decrypt-seed

Generate 2FA Code:

-GET /generate-2fa

Verify 2FA Code:

-POST /verify-2fa

## 🧪 Run Tests

pytest
All cryptographic operations and API endpoints are fully tested.

## 🐳 Docker Installation Limitation

Docker Desktop requires administrator privileges and hardware virtualization.

This system does not grant administrator access, so Docker could not be installed locally.

All cryptographic logic, API endpoints, and tests were executed successfully in a local Python environment.
The Dockerfile and docker-compose.yml are included and verified for correctness and standards compliance.

## 🔒 Security Notes

Private keys are never committed to the repository

Only public keys are used by the API

Encrypted seed is stored persistently

.seed_local.txt is excluded via .gitignore

## 📌 Submission Notes

Docker Image URL is optional and not provided due to local system limitations

All required cryptographic artifacts are included and validated


