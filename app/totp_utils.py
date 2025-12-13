import pyotp


def generate_totp(secret: str):
    return pyotp.TOTP(secret).now()


def verify_totp(secret: str, token: str, window: int):
    return pyotp.TOTP(secret).verify(token, valid_window=window)
