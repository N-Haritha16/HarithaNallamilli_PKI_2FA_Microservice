#!/usr/bin/env python3

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import base64

def encrypt_message(msg: bytes) -> bytes:
    with open("instructor_public.pem", "rb") as f:
        pub = serialization.load_pem_public_key(f.read())

    ct = pub.encrypt(
        msg,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return base64.b64encode(ct)

if __name__ == "__main__":
    data = b"test encryption 256"
    encrypted = encrypt_message(data)
    print(encrypted.decode())
