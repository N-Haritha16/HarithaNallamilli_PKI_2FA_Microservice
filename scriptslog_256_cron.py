#!/usr/bin/env python3

import os
import datetime
import base64
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

# Import your OTP generator (you must have this in your project)
from generator.otp_256 import generate_256_code


# -----------------------------
# Helper: Load Private Key
# -----------------------------
def load_private_key():
    with open("student_private.pem", "rb") as f:
        key_data = f.read()

    return serialization.load_pem_private_key(
        key_data,
        password=None
    )


# -----------------------------
# Helper: Decrypt the seed file
# -----------------------------
def decrypt_seed():
    priv_key = load_private_key()

    with open("encrypted_seed.txt", "rb") as f:
        ciphertext = f.read()

    seed = priv_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return seed


# -----------------------------
# Main Cron Logic
# -----------------------------
def main():

    # 1. read time for protected storage
    now = datetime.datetime.utcnow()

    # 2. open seed/encrypted seed + decrypt seed
    seed = decrypt_seed()

    # 3. generate the correct 256-bit code
    #    using your existing OTP generator function
    code = generate_256_code(seed, now)

    # 4. output directory: /cron/logs/
    log_dir = Path("/cron/logs")
    log_dir.mkdir(parents=True, exist_ok=True)

    # Correct filename using timestamp
    filename = log_dir / f"{now.strftime('%Y%m%d_%H%M%S')}.log"

    # Required output format:
    # "{timestamp} : 256 code: {code}"
    output_line = f"{now.isoformat()} : 256 code: {code}"

    # 5. Write to file
    with open(filename, "w") as f:
        f.write(output_line + "\n")

    # 6. Also print to stdout (cron captures stdout)
    print(output_line)


if __name__ == "__main__":
    main()
