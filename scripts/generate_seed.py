# scripts/generate_seed.py
"""
Generates a base32 TOTP seed and encrypts it with instructor_public.pem
Output: encrypted_seed.txt (SINGLE LINE, base64)
"""

import os
import base64
from pathlib import Path
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

INSTRUCTOR_PUB = Path("instructor_public.pem")
OUT = Path("encrypted_seed.txt")

if not INSTRUCTOR_PUB.exists():
    raise SystemExit("instructor_public.pem not found")

# 1️⃣ Generate TOTP seed (20 bytes → base32)
seed_bytes = os.urandom(20)
seed_base32 = base64.b32encode(seed_bytes)

print("Generated base32 seed (local only):", seed_base32.decode())

# 2️⃣ Load instructor public key
pub = serialization.load_pem_public_key(
    INSTRUCTOR_PUB.read_bytes()
)

# 3️⃣ Encrypt seed using RSA OAEP SHA256
encrypted = pub.encrypt(
    seed_base32,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None,
    ),
)

# 4️⃣ Write SINGLE-LINE base64 output
OUT.write_text(base64.b64encode(encrypted).decode())

# 5️⃣ Optional local testing seed (DO NOT COMMIT)
Path(".seed_local.txt").write_text(seed_base32.decode())

print("encrypted_seed.txt written (single line)")
print(".seed_local.txt written (DO NOT COMMIT)")
