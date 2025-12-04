#!/usr/bin/env python3
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

def sign_message(msg: bytes) -> bytes:
    with open("student_private.pem", "rb") as f:
        priv = serialization.load_pem_private_key(f.read(), password=None)

    sig = priv.sign(
        msg,
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    return sig

if __name__ == "__main__":
    data = b"test signature 256"
    sig = sign_message(data)
    print(sig.hex())
