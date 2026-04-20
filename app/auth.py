from jose import jwt
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
    
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models

security = HTTPBearer()

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        if user_id is None:
            raise Exception("Invalid token")

        return user_id

    except JWTError:
        raise Exception("Token is invalid or expired")


def get_current_user( credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials

    try:
        user_id = verify_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

def require_role(required_role: str):

    def role_checker(current_user: models.User = Depends(get_current_user)):

        if current_user.role != required_role:
            raise HTTPException(
                status_code=403,
                detail="Not authorized"
            )

        return current_user

    return role_checker