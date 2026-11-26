import jwt

from fastapi.security import HTTPBearer
from fastapi import Depends, HTTPException
from app.auth.routes import JWT_SECRET, users_db

bearer = HTTPBearer(auto_error=False)

def get_current_user(credentials=Depends(bearer)):
    if not credentials:
        raise HTTPException(401, "Token is required.")

    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=["HS256"])

        user = users_db.get(payload["sub"])

        if not user:
            raise HTTPException(404, "User not found.")

        return user

    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid or expired token")