import base64
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .config import SEED_PATH, INSTRUCTOR_PUBLIC_KEY, INSTRUCTOR_PRIVATE_KEY, TOTP_WINDOW


from .crypto_utils import decrypt_seed, verify_signature
from .totp_utils import generate_totp, verify_totp

app = FastAPI(title="PKI 2FA Microservice")


class VerifyCodeRequest(BaseModel):
    code: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/decrypt-seed")
def decrypt_seed_endpoint():
    """
    Verifies the seed signature and decrypts it using the private key.
    Returns the actual seed.
    """
    if not SEED_PATH.exists() or not SEED_SIG_PATH.exists():
        raise HTTPException(status_code=404, detail="Seed file or signature not found")

    # Verify seed signature
    seed_bytes = SEED_PATH.read_bytes()
    sig_text = SEED_SIG_PATH.read_text()
    if not verify_signature(seed_bytes, sig_text, INSTRUCTOR_PUBLIC_KEY):
        raise HTTPException(status_code=400, detail="Seed signature invalid")

    # Decrypt seed
    try:
        seed = decrypt_seed(SEED_PATH, INSTRUCTOR_PRIVATE_KEY)
        return {"seed": seed.decode()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to decrypt seed: {e}")


@app.get("/generate-2fa")
def generate_2fa():
    """
    Generates a TOTP code from the decrypted seed.
    """
    if not SEED_PATH.exists() or not SEED_SIG_PATH.exists():
        raise HTTPException(status_code=400, detail="Seed not initialized")

    try:
        seed_bytes = decrypt_seed(SEED_PATH, INSTRUCTOR_PRIVATE_KEY)
        secret = base64.b32encode(seed_bytes).decode()
        code = generate_totp(secret)
        return {"code": code}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/verify-2fa")
def verify_2fa_endpoint(req: VerifyCodeRequest):
    """
    Verifies a submitted TOTP code using the decrypted seed.
    """
    if not SEED_PATH.exists() or not SEED_SIG_PATH.exists():
        raise HTTPException(status_code=400, detail="Seed not initialized")

    try:
        seed_bytes = decrypt_seed(SEED_PATH, INSTRUCTOR_PRIVATE_KEY)
        secret = base64.b32encode(seed_bytes).decode()
        valid = verify_totp(secret, req.code, TOTP_WINDOW)
        return {"valid": valid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
