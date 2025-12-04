🔐 PKI-Based 2FA Microservice (Dockerized)

A secure Two-Factor Authentication (2FA) microservice built using Public Key Infrastructure (PKI), RSA encryption, TOTP (Time-based OTP), and Docker.
This project demonstrates strong concepts in backend development, security, cryptography, Docker, cron automation, and REST API design.

🚀 Features
🔑 PKI & RSA Security

Generates RSA private/public key pairs

Secure key storage using Docker volume

Supports RSA signing & verification

⏱️ TOTP Authentication

6-digit OTP generation (valid 30 seconds)

RFC-6238 compliant

Works with Google Authenticator, Authy, etc.

🐳 Dockerized Microservice

Multi-stage Docker build

Lightweight final image

Cron job for automatic key rotation

Supports persistent data storage

📡 REST API

/generate-key – Creates RSA keys

/generate-totp – Issues TOTP secret + QR URL

/verify-totp – Validates entered OTP

🐳 Docker Setup
Build Image

Run Container

Run with Persistent Volume (Recommended)

Cron Job Setup Inside Docker

The cron script runs daily at midnight

Automatically rotates RSA keys

📡 API Endpoints
▶️ Generate RSA Keys
POST /generate-key

▶️ Generate TOTP
POST /generate-totp

▶️ Verify OTP
POST /verify-totp

▶️ Sign Data
POST /sign

▶️ Verify Signature
POST /verify-signature

🔧 Technologies Used

Python / FastAPI (or Express/Go/Rust depending on stack)

Docker (Multi-stage builds)

PKI / RSA / OpenSSL

TOTP (RFC 6238)

Linux Cron

Persistent Volume Storage

🎯 Learning Outcomes

By completing the project, you learn:

How PKI and RSA encryption work

How to build secure authentication microservices

How TOTP is generated & verified

How to create Docker multi-stage builds

How cron jobs run inside Linux containers

How to manage secure key storage

This project is perfect for resume, DevOps preparation, backend interviews, and security engineering practice.

📄 License

This project is for educational and development use.

If you'd like, I can also generate:
✨ GitHub badges (build, license, tech used)
✨ Architecture diagram (SVG)
✨ API documentation table
✨ A more stylish README with emojis and color sections

/sign – Sign a payload

/verify-signature – Validate signatures
