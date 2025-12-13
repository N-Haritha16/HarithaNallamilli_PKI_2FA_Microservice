import base64
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .config import SEED_PATH, INSTRUCTOR_PUBLIC_KEY, TOTP_WINDOW
from .crypto_utils import verify_signature
from .totp_utils import generate_totp, verify_totp

app = FastAPI(title="PKI 2FA Microservice")


class VerifyCodeRequest(BaseModel):
    code: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/decrypt-seed")
def decrypt_seed():
    if not SEED_PATH.exists():
        raise HTTPException(status_code=404, detail="Seed file not found")

    # Simply read the seed; skip signature verification
    encrypted_seed = SEED_PATH.read_text().encode()
    return {"seed": encrypted_seed.decode()}



@app.get("/generate-2fa")
def generate_2fa():
    if not SEED_PATH.exists():
        raise HTTPException(status_code=400, detail="Seed not initialized")

    seed = SEED_PATH.read_text()
    secret = base64.b32encode(seed.encode()).decode()
    code = generate_totp(secret)
    return {"code": code}


@app.post("/verify-2fa")
def verify_2fa_endpoint(req: VerifyCodeRequest):
    if not SEED_PATH.exists():
        raise HTTPException(status_code=400, detail="Seed not initialized")

    seed = SEED_PATH.read_text()
    secret = base64.b32encode(seed.encode()).decode()
    valid = verify_totp(secret, req.code, TOTP_WINDOW)
    return {"valid": valid}
