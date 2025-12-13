#!/usr/bin/env python3
import base64
from datetime import datetime, timezone
from pathlib import Path

from app.totp_utils import generate_totp
from app.config import SEED_PATH

def main():
    try:
        # 1. Read hex seed from persistent storage
        # SEED_PATH is the same path used by the FastAPI app (e.g., /data/seed.txt)
        if not SEED_PATH.exists():
            print("Seed file not found")
            return

        seed = SEED_PATH.read_text().strip()
        if not seed:
            print("Seed file is empty")
            return

        # 2. Generate current TOTP code
        # Convert seed string to base32 and generate TOTP
        secret = base64.b32encode(seed.encode()).decode()
        code = generate_totp(secret)

        # 3. Get current UTC timestamp
        now_utc = datetime.now(timezone.utc)
        timestamp = now_utc.strftime("%Y-%m-%d %H:%M:%S")

        # 4. Output formatted line
        print(f"{timestamp} - 2FA Code: {code}")

    except Exception as e:
        # Log any unexpected error so you can debug cron
        print(f"Error generating 2FA code: {e}")

if __name__ == "__main__":
    main()
