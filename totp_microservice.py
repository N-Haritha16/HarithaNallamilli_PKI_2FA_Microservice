import pyotp
from data.seed import user_secrets
  # Import the dictionary

# ---------------------------
# Endpoint 1: Generate/Request Seed
# ---------------------------
def endpoint_generate_seed(user_id):
    """Generate or retrieve secret key for a user"""
    if user_id not in user_secrets:
        # Generate a random base32 secret for the user
        secret = pyotp.random_base32()
        user_secrets[user_id] = secret
    else:
        secret = user_secrets[user_id]
    print(f"[Endpoint 1] Secret for user {user_id}: {secret}")
    return secret

# ---------------------------
# Endpoint 2: Generate TOTP
# ---------------------------
def endpoint_generate_totp(user_id):
    """Generate current TOTP for a user"""
    if user_id not in user_secrets:
        print(f"[Endpoint 2] Error: user {user_id} not found.")
        return None
    secret = user_secrets[user_id]
    totp = pyotp.TOTP(secret)
    otp = totp.now()
    print(f"[Endpoint 2] Generated TOTP for user {user_id}: {otp}")
    return otp

# ---------------------------
# Endpoint 3: Verify TOTP
# ---------------------------
def endpoint_verify_totp(user_id, otp):
    """Verify the TOTP code for a user"""
    if user_id not in user_secrets:
        print(f"[Endpoint 3] Error: user {user_id} not found.")
        return False
    secret = user_secrets[user_id]
    totp = pyotp.TOTP(secret)
    valid = totp.verify(otp)
    print(f"[Endpoint 3] Verification result for {user_id}: {valid}")
    return valid

# ---------------------------
# Demo flow
# ---------------------------
if __name__ == "__main__":
    user_id = input("Enter your user_id: ").strip()

    # Endpoint 1: Generate/Request seed
    endpoint_generate_seed(user_id)

    # Endpoint 2: Generate TOTP
    otp = endpoint_generate_totp(user_id)

    # Endpoint 3: Verify TOTP
    endpoint_verify_totp(user_id, otp)
