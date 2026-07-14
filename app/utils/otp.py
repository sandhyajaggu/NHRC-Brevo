import random

from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)



def verify_value(value: str, hashed: str) -> bool:
    return pwd_context.verify(value, hashed)

def generate_random_otp(length: int = 6) -> str:
    """
    Generate a numeric OTP.
    Example: 483921
    """
    return "".join(random.choices("0123456789", k=length))