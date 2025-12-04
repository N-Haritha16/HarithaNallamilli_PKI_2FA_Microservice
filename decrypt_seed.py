import os
import json
import base64
import requests
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

# ===============================
# CONFIGURATION
# ===============================
STUDENT_ID = "23P31A12B0"
GITHUB_REPO_URL = "https://github.com/N-Haritha16/HarithaNallamilli_PKI_2FA_Microservice"
API_URL = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws/"  # Replace with actual API URL

PRIVATE_KEY_FILE = "student_private.pem"
PUBLIC_KEY_FILE = "student_public.pem"
OUTPUT_SEED_FILE = os.path.join("data", "seed.txt")
ENCRYPTED_FILE = "encrypted_seed.txt"

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

# ===============================
# Load Private Key
# ===============================
def load_private_key():
    with open(PRIVATE_KEY_FILE, "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)

# ===============================
# Load Public Key as String
# ===============================
def load_public_key():
    with open(PUBLIC_KEY_FILE, "r") as f:
        return f.read()

# ===============================
# Request Encrypted Seed
# ===============================
def request_encrypted_seed(student_id, github_repo_url, public_key, api_url):
    payload = {
        "student_id": student_id,
        "github_repo_url": github_repo_url,
        "public_key": public_key
    }

    print("Requesting encrypted seed from instructor API...")
    response = requests.post(api_url, json=payload, timeout=10)

    if response.status_code != 200:
        raise Exception(f"API request failed: {response.status_code} - {response.text}")

    data = response.json()
    if "encrypted_seed" not in data:
        raise Exception("'encrypted_seed' not found in API response.")

    encrypted_seed = data["encrypted_seed"]

    # Save encrypted seed for reference
    with open(ENCRYPTED_FILE, "w") as f:
        f.write(encrypted_seed)

    print("Encrypted seed received and saved.")
    return encrypted_seed

# ===============================
# Decrypt Seed
# ===============================
def decrypt_seed(encrypted_seed_b64, private_key):
    encrypted_bytes = base64.b64decode(encrypted_seed_b64)
    decrypted_bytes = private_key.decrypt(
        encrypted_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_bytes.decode()

# ===============================
# Generate 64-bit Seed
# ===============================
def generate_64bit_seed(raw_seed):
    combined = f"{raw_seed}-{STUDENT_ID}-{GITHUB_REPO_URL}"
    return combined.encode()[:8].hex()  # First 8 bytes = 64 bits

# ===============================
# MAIN
# ===============================
def main():
    private_key = load_private_key()
    public_key = load_public_key()

    encrypted_seed_b64 = request_encrypted_seed(STUDENT_ID, GITHUB_REPO_URL, public_key, API_URL)

    raw_seed = decrypt_seed(encrypted_seed_b64, private_key)
    print("Decrypted raw seed:", raw_seed)

    final_seed = generate_64bit_seed(raw_seed)

    with open(OUTPUT_SEED_FILE, "w") as f:
        f.write(final_seed)

    print(f"Final 64-bit seed stored at: {OUTPUT_SEED_FILE}")
    print("Final Seed:", final_seed)

if __name__ == "__main__":
    main()
