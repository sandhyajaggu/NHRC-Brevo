import random


def generate_random_otp(length: int = 6) -> str:
    """
    Generate a numeric OTP.
    Example: 483921
    """
    return "".join(random.choices("0123456789", k=length))