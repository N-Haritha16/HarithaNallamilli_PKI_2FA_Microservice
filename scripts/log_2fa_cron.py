#!/usr/bin/env python3

import sys
import base64
from datetime import datetime, timezone
from pathlib import Path

from app.totp_utils import generate_totp
from app.config import SEED_PATH

# Corrected path for log file (relative to project directory)
LOG_PATH = Path("cron/last_code.txt")


def debug(msg):
    """Print debug messages to stderr for cron logs"""
    print(f"[DEBUG] {msg}", file=sys.stderr)


def main():
    try:
        debug("Starting cron job")

        # 1. Check seed file
        if not SEED_PATH.exists():
            raise FileNotFoundError(f"Seed file not found at {SEED_PATH}")
        debug(f"Seed file exists: {SEED_PATH}")

        # 2. Read seed
        seed_b64 = SEED_PATH.read_text(encoding="utf-8").strip()
        if not seed_b64:
            raise ValueError("Seed file is empty")
        debug(f"Seed read successfully: {seed_b64[:8]}...")

        # 3. Decode BASE64 → bytes
        seed_bytes = base64.b64decode(seed_b64)
        debug(f"Seed decoded to bytes: {seed_bytes[:8]}...")

        # 4. Convert to Base32 for TOTP
        secret = base64.b32encode(seed_bytes).decode("ascii")
        debug(f"Secret Base32: {secret[:8]}...")

        # 5. Generate TOTP
        code = generate_totp(secret)
        debug(f"TOTP code generated: {code}")

        # 6. UTC timestamp
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"{timestamp} - 2FA Code: {code}\n"

        # 7. Ensure log directory exists
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        debug(f"Writing log to {LOG_PATH.resolve()}")

        # 8. Write log
        with LOG_PATH.open("a", encoding="utf-8") as f:
            f.write(log_line)
            f.flush()  # Ensure data is written immediately

        debug("Log written successfully")

    except Exception as e:
        print(f"[CRON ERROR] {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
