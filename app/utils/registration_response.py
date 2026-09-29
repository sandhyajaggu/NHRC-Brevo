SENSITIVE_WORDS = ("password", "otp", "captcha")


def model_to_dict(obj):
    """Return every column of a SQLAlchemy row, skipping secrets."""
    if obj is None:
        return None

    return {
        column.name: getattr(obj, column.name)
        for column in obj.__table__.columns
        if not any(word in column.name.lower() for word in SENSITIVE_WORDS)
    }


def registration_response(member, details):
    """
    Common response for membership registration endpoints:
    the member's personal details plus the type-specific details.
    """
    return {
        "member": model_to_dict(member),
        "details": model_to_dict(details),
    }
