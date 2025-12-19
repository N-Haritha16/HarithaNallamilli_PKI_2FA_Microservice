import base64
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .config import SEED_PATH, STUDENT_PUBLIC_KEY, TOTP_WINDOW, STUDENT_PRIVATE_KEY
from .crypto_utils import verify_signature, decrypt_with_private_key
from .totp_utils import generate_totp, verify_totp

app = FastAPI(title="PKI 2FA Microservice")

# Path to store the decrypted seed separately
DECRYPTED_SEED_PATH = SEED_PATH.parent / "decrypted_seed.txt"


# -----------------------------
# Request models
# -----------------------------
class SeedRequest(BaseModel):
    encrypted_seed: str
    signature: str


class DecryptSeedRequest(BaseModel):
    encrypted_seed: str  # base64-encoded


class VerifyRequest(BaseModel):
    token: str


# -----------------------------
# Health check endpoint
# -----------------------------
@app.get("/health")
def health():
    return {"status": "ok"}


# -----------------------------
# Accept encrypted seed and verify signature
# -----------------------------
@app.post("/accept-seed")
def accept_seed(req: SeedRequest):
    print("DEBUG: /accept-seed called")

    # Verify signature
    if not verify_signature(
        req.encrypted_seed.encode(),
        req.signature,
        STUDENT_PUBLIC_KEY,
    ):
        print("DEBUG: Signature verification FAILED")
        raise HTTPException(status_code=401, detail="Invalid signature")

    # Store encrypted seed
    SEED_PATH.write_text(req.encrypted_seed)
    print("DEBUG: Encrypted seed stored successfully at", SEED_PATH)

    return {"status": "seed stored"}


# -----------------------------
# Decrypt the stored seed
# -----------------------------
@app.post("/decrypt-seed")
def decrypt_seed(req: DecryptSeedRequest):
    print("DEBUG: /decrypt-seed called")

    try:
        # Step 1: Base64 decode incoming encrypted seed
        encrypted_bytes = base64.b64decode(req.encrypted_seed)
        print("DEBUG: Base64 decoded length:", len(encrypted_bytes))

        # Step 2: Decrypt with RSA private key
        decrypted_seed = decrypt_with_private_key(
            encrypted_bytes,
            STUDENT_PRIVATE_KEY,
        )
        print("DEBUG: Decryption successful")
        print("DEBUG: Decrypted seed (first 50 bytes):", decrypted_seed[:50])

        # Step 3: Encode decrypted seed safely (base64)
        safe_seed = base64.b64encode(decrypted_seed).decode("ascii")
        print("DEBUG: Decrypted seed (base64):", safe_seed)

        # Step 4: Store decrypted seed separately
        DECRYPTED_SEED_PATH.write_text(safe_seed)
        print("DEBUG: Decrypted seed stored successfully at", DECRYPTED_SEED_PATH)

        return {"status": "ok", "decrypted_seed": safe_seed}

    except Exception as e:
        print("DEBUG: Decryption FAILED with error:", repr(e))
        raise HTTPException(
            status_code=500,
            detail={"error": "Decryption failed"},
        )


# -----------------------------
# Generate TOTP token
# -----------------------------
@app.get("/generate-2fa")
def generate_2fa():
    if not DECRYPTED_SEED_PATH.exists():
        raise HTTPException(status_code=400, detail="Seed not decrypted yet")

    # Read base64 seed and decode to bytes
    seed_b64 = DECRYPTED_SEED_PATH.read_text()
    seed_bytes = base64.b64decode(seed_b64)

    # Convert to base32 for TOTP
    secret = base64.b32encode(seed_bytes).decode("ascii")
    token = generate_totp(secret)
    return {"token": token}


# -----------------------------
# Verify TOTP token
# -----------------------------
@app.post("/verify-2fa")
def verify_2fa_endpoint(req: VerifyRequest):
    if not DECRYPTED_SEED_PATH.exists():
        raise HTTPException(status_code=400, detail="Seed not decrypted yet")

    # Read decrypted seed
    seed_b64 = DECRYPTED_SEED_PATH.read_text()
    seed_bytes = base64.b64decode(seed_b64)

    secret = base64.b32encode(seed_bytes).decode("ascii")
    is_valid = verify_totp(secret, req.token, TOTP_WINDOW)
    return {"valid": is_valid}
