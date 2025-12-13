from pathlib import Path

DATA_DIR = Path("/app/data")
SEED_PATH = DATA_DIR / "seed.txt"
SIG_PATH = DATA_DIR / "seed.sig"

STUDENT_PUBLIC_KEY = Path("/app/student_public.pem")
INSTRUCTOR_PUBLIC_KEY = Path("/app/instructor_public.pem")

TOTP_WINDOW = 1
