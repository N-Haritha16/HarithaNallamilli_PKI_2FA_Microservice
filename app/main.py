import base64
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .config import (
    SEED_PATH,
    STUDENT_PUBLIC_KEY,
    TOTP_WINDOW,
)
from .crypto_utils import verify_signature
from .totp_utils import generate_totp, verify_totp

app = FastAPI(title="PKI 2FA Microservice")


class SeedRequest(BaseModel):
    encrypted_seed: str
    signature: str


class VerifyRequest(BaseModel):
    token: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/decrypt-seed")
def decrypt_seed(req: SeedRequest):
    if not verify_signature(
        req.encrypted_seed.encode(),
        req.signature,
        STUDENT_PUBLIC_KEY,
    ):
        raise HTTPException(status_code=401, detail="Invalid signature")

    SEED_PATH.write_text(req.encrypted_seed)
    return {"status": "seed stored"}


@app.get("/generate-2fa")
def generate_2fa():
    if not SEED_PATH.exists():
        raise HTTPException(400, "Seed not initialized")

    seed = SEED_PATH.read_text()
    secret = base64.b32encode(seed.encode()).decode()
    return {"token": generate_totp(secret)}


@app.post("/verify-2fa")
def verify_2fa_endpoint(req: VerifyRequest):
    if not SEED_PATH.exists():
        raise HTTPException(400, "Seed not initialized")

    seed = SEED_PATH.read_text()
    secret = base64.b32encode(seed.encode()).decode()
    return {
        "valid": verify_totp(secret, req.token, TOTP_WINDOW)
    }
