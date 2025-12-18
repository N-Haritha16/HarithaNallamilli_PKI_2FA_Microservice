import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature


# ---------- Key Loaders ----------

def load_public_key(path):
    """
    Load an RSA public key from a PEM file.
    """
    return serialization.load_pem_public_key(
        path.read_bytes()
    )


def load_private_key(path):
    """
    Load an RSA private key from a PEM file.
    Assumes the key is NOT password protected.
    """
    return serialization.load_pem_private_key(
        path.read_bytes(),
        password=None,
    )


# ---------- Signature Verification ----------

def verify_signature(data: bytes, signature_b64: str, public_key_path) -> bool:
    """
    Verify RSA-PSS + SHA256 signature.
    """
    public_key = load_public_key(public_key_path)

    try:
        public_key.verify(
            base64.b64decode(signature_b64),
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
        return True

    except InvalidSignature:
        return False


# ---------- Decryption (Option 1: OAEP + SHA256) ----------

def decrypt_with_private_key(ciphertext: bytes, private_key_path) -> bytes:
    private_key = load_private_key(private_key_path)

    # Try OAEP + SHA256 (preferred)
    try:
        return private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
    except ValueError:
        # Fallback to PKCS1v15 (legacy support)
        return private_key.decrypt(
            ciphertext,
            padding.PKCS1v15(),
        )


# import base64
# from cryptography.hazmat.primitives import hashes, serialization
# from cryptography.hazmat.primitives.asymmetric import padding
# from cryptography.exceptions import InvalidSignature


# def load_public_key(path):
#     return serialization.load_pem_public_key(path.read_bytes())


# def verify_signature(data: bytes, signature_b64: str, pub_path):
#     public_key = load_public_key(pub_path)
#     try:
#         public_key.verify(
#             base64.b64decode(signature_b64),
#             data,
#             padding.PSS(
#                 mgf=padding.MGF1(hashes.SHA256()),
#                 salt_length=padding.PSS.MAX_LENGTH,
#             ),
#             hashes.SHA256(),
#         )
#         return True
#     except InvalidSignature:
#         return False
    

# def load_private_key(path):
#     return serialization.load_pem_private_key(
#         path.read_bytes(),
#         password=None,  # assuming no passphrase
#     )


# def decrypt_with_private_key(ciphertext: bytes, private_key_path):
#     private_key = load_private_key(private_key_path)
#     return private_key.decrypt(
#         ciphertext,
#         padding.OAEP(
#             mgf=padding.MGF1(algorithm=hashes.SHA256()),
#             algorithm=hashes.SHA256(),
#             label=None,
#         ),
#     )

