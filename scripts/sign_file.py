import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

with open("student_private.pem", "rb") as f:
    priv = serialization.load_pem_private_key(f.read(), password=None)

data = open("encrypted_seed.txt", "rb").read()

sig = priv.sign(
    data,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH,
    ),
    hashes.SHA256(),
)

with open("encrypted_seed.sig", "w") as f:
    f.write(base64.b64encode(sig).decode())
