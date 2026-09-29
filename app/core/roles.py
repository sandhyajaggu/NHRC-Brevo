from fastapi import Depends, HTTPException
from app.core.dependencies import get_current_user


def require_role(required_role: str):
    def role_checker(current_user = Depends(get_current_user)):
        if (current_user.role or "").strip().upper() != required_role.strip().upper():
            raise HTTPException(status_code=403, detail="Access denied")
        return current_user
    return role_checker