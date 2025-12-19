import base64
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .config import SEED_PATH, STUDENT_PUBLIC_KEY, TOTP_WINDOW, STUDENT_PRIVATE_KEY
from .crypto_utils import verify_signature,decrypt_with_private_key
from .totp_utils import generate_totp, verify_totp

app = FastAPI(title="PKI 2FA Microservice")


class SeedRequest(BaseModel):
    encrypted_seed: str
    signature: str


class VerifyRequest(BaseModel):
    token: str

class DecryptSeedRequest(BaseModel):
    encrypted_seed: str  # base64-encoded


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/accept-seed")
def accept_seed(req: SeedRequest):
    print("DEBUG: /accept-seed called")

    if not verify_signature(
        req.encrypted_seed.encode(),
        req.signature,
        STUDENT_PUBLIC_KEY,
    ):
        print("DEBUG: Signature verification FAILED")
        raise HTTPException(status_code=401, detail="Invalid signature")

    SEED_PATH.write_text(req.encrypted_seed)
    print("DEBUG: Encrypted seed stored successfully",SEED_PATH.write_text(req.encrypted_seed))

    return {"status": "seed stored"}

@app.post("/decrypt-seed")
def decrypt_seed(req: DecryptSeedRequest):
    print("DEBUG: /decrypt-seed called")

    try:
        # Step 1: Base64 decode incoming encrypted seed
        encrypted_bytes = base64.b64decode(req.encrypted_seed)
        print("DEBUG: Base64 decoded length:", len(encrypted_bytes))

        # Step 2: Decrypt
        decrypted_seed = decrypt_with_private_key(
            encrypted_bytes,
            STUDENT_PRIVATE_KEY,
        )
        print("DEBUG: Decryption successful")
        print("DEBUG: Decrypted seed (raw bytes):", decrypted_seed)

        # ✅ Step 3: Encode decrypted seed safely (BASE64)
        safe_seed = base64.b64encode(decrypted_seed).decode("ascii")
        print("DEBUG: Decrypted seed (base64):", safe_seed)

        # Step 4: Store base64 seed
        SEED_PATH.write_text(safe_seed)
        print("DEBUG: Seed stored successfully")

        return {"status": "ok"}

    except Exception as e:
        print("DEBUG: Decryption FAILED with error:", repr(e))
        raise HTTPException(
            status_code=500,
            detail={"error": "Decryption failed"},
        )



# @app.get("/generate-2fa")
# def generate_2fa():
#     if not SEED_PATH.exists():
#         raise HTTPException(status_code=400, detail="Seed not initialized")

#     seed = SEED_PATH.read_text()
#     secret = base64.b32encode(seed.encode()).decode()
#     return {"token": generate_totp(secret)}
@app.get("/generate-2fa")
def generate_2fa():
    if not SEED_PATH.exists():
        raise HTTPException(status_code=400, detail="Seed not initialized")

    # Read base64 seed and decode to bytes
    seed_b64 = SEED_PATH.read_text()
    seed_bytes = base64.b64decode(seed_b64)

    # Convert to base32 for TOTP
    secret = base64.b32encode(seed_bytes).decode("ascii")
    return {"token": generate_totp(secret)}




# @app.post("/verify-2fa")
# def verify_2fa_endpoint(req: VerifyRequest):
#     if not SEED_PATH.exists():
#         raise HTTPException(status_code=400, detail="Seed not initialized")

#     seed = SEED_PATH.read_text()
#     secret = base64.b32encode(seed.encode()).decode()
#     return {"valid": verify_totp(secret, req.token, TOTP_WINDOW)}
@app.post("/verify-2fa")
def verify_2fa_endpoint(req: VerifyRequest):
    if not SEED_PATH.exists():
        raise HTTPException(status_code=400, detail="Seed not initialized")

    seed_b64 = SEED_PATH.read_text()
    seed_bytes = base64.b64decode(seed_b64)

    secret = base64.b32encode(seed_bytes).decode("ascii")
    return {"valid": verify_totp(secret, req.token, TOTP_WINDOW)}
