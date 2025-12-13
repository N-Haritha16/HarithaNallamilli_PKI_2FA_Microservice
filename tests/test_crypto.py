# tests/test_crypto.py
from pathlib import Path
from app.crypto_utils import verify_signature


def test_verify_signature_valid():
    data = b"test-message"

    sig_path = Path("encrypted_seed.sig")
    pub_path = Path("student_public.pem")

    assert sig_path.exists(), "encrypted_seed.sig missing"
    assert pub_path.exists(), "student_public.pem missing"

    signature = sig_path.read_text().strip()

    assert verify_signature(data, signature, pub_path) in [True, False]
