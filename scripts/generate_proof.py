#!/usr/bin/env python3

import hashlib
import json
from pathlib import Path
from sign_message import sign_message
from encrypt_message import encrypt_message

def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def compute_merkle_root(codes):
    if len(codes) == 1:
        return sha256_hex(codes[0].encode())

    new = []
    for i in range(0, len(codes), 2):
        left = codes[i]
        right = codes[i+1] if i+1 < len(codes) else codes[i]
        combined = (left + right).encode()
        new.append(sha256_hex(combined))

    return compute_merkle_root(new)

def load_codes():
    log_files = sorted(Path("/cron/logs").glob("*.log"))
    codes = []
    for lf in log_files:
        with open(lf) as f:
            line = f.read().strip()
            # expected: "timestamp : 256 code: XXXXXX"
            code = line.split("256 code:")[1].strip()
            codes.append(code)
    return codes

if __name__ == "__main__":
    codes = load_codes()

    root = compute_merkle_root(codes)
    signature = sign_message(root.encode()).hex()
    ciphertext = encrypt_message(root.encode()).decode()

    proof = {
        "merkleRoot": root,
        "rootSignature": signature,
        "rootCipherText": ciphertext,
        "student": "YOUR_STUDENT_ID"
    }

    print(json.dumps(proof, indent=4))
