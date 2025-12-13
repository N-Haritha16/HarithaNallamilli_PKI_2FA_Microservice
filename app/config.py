from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = Path("/data")
DATA_DIR.mkdir(exist_ok=True)

SEED_PATH = DATA_DIR / "seed.txt"

STUDENT_PUBLIC_KEY = BASE_DIR / "student_public.pem"
INSTRUCTOR_PUBLIC_KEY = BASE_DIR / "instructor_public.pem"

TOTP_WINDOW = 1
