from pathlib import Path

BASE_DIR = Path(__file__).parent

# Paths to seed files
SEED_PATH = BASE_DIR / "data/encrypted_seed.txt"
SEED_SIG_PATH = BASE_DIR / "data/encrypted_seed.sig"   # <-- add this

# Paths to keys
INSTRUCTOR_PRIVATE_KEY = BASE_DIR / "instructor_private.pem"
INSTRUCTOR_PUBLIC_KEY = BASE_DIR / "instructor_public.pem"

# TOTP settings
TOTP_WINDOW = 1  # valid code window
