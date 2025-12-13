from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def gen_keypair(name):
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    with open(f"{name}_private.pem", "wb") as f:
        f.write(
            key.private_bytes(
                serialization.Encoding.PEM,
                serialization.PrivateFormat.TraditionalOpenSSL,
                serialization.NoEncryption(),
            )
        )

    with open(f"{name}_public.pem", "wb") as f:
        f.write(
            key.public_key().public_bytes(
                serialization.Encoding.PEM,
                serialization.PublicFormat.SubjectPublicKeyInfo,
            )
        )

gen_keypair("student")
gen_keypair("instructor")
