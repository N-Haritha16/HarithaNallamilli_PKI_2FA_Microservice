import base64
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .config import SEED_PATH, STUDENT_PUBLIC_KEY, TOTP_WINDOW, STUDENT_PRIVATE_KEY
from .crypto_utils import verify_signature, decrypt_with_private_key
from .totp_utils import generate_totp, verify_totp

app = FastAPI(title="PKI 2FA Microservice")


# -------------------- Models --------------------

class SeedRequest(BaseModel):
    encrypted_seed: str
    signature: str


class DecryptSeedRequest(BaseModel):
    encrypted_seed: str  # base64-encoded RSA ciphertext


class VerifyRequest(BaseModel):
    token: str


# -------------------- Health --------------------

@app.get("/health")
def health():
    return {"status": "ok"}


# -------------------- Seed Handling --------------------

@app.post("/accept-seed")
def accept_seed(req: SeedRequest):
    print("DEBUG: /accept-seed called")

    if not verify_signature(
        req.encrypted_seed.encode("utf-8"),
        req.signature,
        STUDENT_PUBLIC_KEY,
    ):
        raise HTTPException(status_code=401, detail="Invalid signature")

    SEED_PATH.write_text(req.encrypted_seed)
    SEED_PATH.chmod(0o600)

    print("DEBUG: Encrypted seed stored successfully")
    return {"status": "seed stored"}


@app.post("/decrypt-seed")
def decrypt_seed(req: DecryptSeedRequest):
    print("DEBUG: /decrypt-seed called")

    try:
        # Decode base64 ciphertext
        encrypted_bytes = base64.b64decode(req.encrypted_seed)

        # RSA decrypt
        decrypted_seed = decrypt_with_private_key(
            encrypted_bytes,
            STUDENT_PRIVATE_KEY,
        )

        # Store seed safely as BASE64
        seed_b64 = base64.b64encode(decrypted_seed).decode("ascii")
        SEED_PATH.write_text(seed_b64)
        SEED_PATH.chmod(0o600)

        print("DEBUG: Seed decrypted and stored successfully")
        return {"status": "ok"}

    except Exception as e:
        print("DEBUG: Decryption FAILED:", repr(e))
        raise HTTPException(
            status_code=500,
            detail="Decryption failed",
        )


# -------------------- 2FA --------------------

@app.get("/generate-2fa")
def generate_2fa():
    if not SEED_PATH.exists():
        raise HTTPException(status_code=400, detail="Seed not initialized")

    seed_b64 = SEED_PATH.read_text()
    seed_bytes = base64.b64decode(seed_b64)

    secret = base64.b32encode(seed_bytes).decode("ascii")
    return {"token": generate_totp(secret)}


@app.post("/verify-2fa")
def verify_2fa_endpoint(req: VerifyRequest):
    if not SEED_PATH.exists():
        raise HTTPException(status_code=400, detail="Seed not initialized")

    seed_b64 = SEED_PATH.read_text()
    seed_bytes = base64.b64decode(seed_b64)

    secret = base64.b32encode(seed_bytes).decode("ascii")
    return {"valid": verify_totp(secret, req.token, TOTP_WINDOW)}
