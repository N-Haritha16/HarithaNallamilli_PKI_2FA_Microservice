import base64
import pyotp

def generate_totp_code(hex_seed: str) -> str:
    """
    Generate current TOTP code from hex seed.
    Args:
        hex_seed: 64-character hex string
    Returns:
        6-digit TOTP code as string
    """
    # Convert hex → bytes
    seed_bytes = bytes.fromhex(hex_seed)
    # Convert bytes → base32 (required for TOTP)
    seed_base32 = base64.b32encode(seed_bytes).decode('utf-8')
    # Create TOTP object
    totp = pyotp.TOTP(seed_base32, digits=6, interval=30, digest='sha1')
    # Generate current TOTP code
    return totp.now()

def verify_totp_code(hex_seed: str, code: str, valid_window: int = 1) -> bool:
    """
    Verify a TOTP code with time tolerance.
    Args:
        hex_seed: 64-character hex seed
        code: 6-digit code user enters
        valid_window: number of 30-sec windows before/after to allow
    Returns:
        True if code is valid, False otherwise
    """
    # Convert hex → bytes
    seed_bytes = bytes.fromhex(hex_seed)
    # Convert bytes → base32
    seed_base32 = base64.b32encode(seed_bytes).decode('utf-8')
    # Create TOTP object
    totp = pyotp.TOTP(seed_base32, digits=6, interval=30, digest='sha1')
    # Verify code
    return totp.verify(code, valid_window=valid_window)
