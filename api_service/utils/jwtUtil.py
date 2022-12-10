import jwt
import os
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from pydantic import ValidationError
from utils import constantUtil
from auth import schemas
from auth import crud

JWT_SECRET_KEY = os.environ["SECRET_KEY"]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_token_user(token: str = Depends(oauth2_scheme)):
    return token


async def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=constantUtil.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, JWT_SECRET_KEY, algorithm=constantUtil.ALGORITHM
    )
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    logout_list = await crud.find_token_logout_lists(token)
    if logout_list:
        raise credentials_exception

    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[constantUtil.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(phone_number=username)
    except (PyJWTError, ValidationError):
        raise credentials_exception

    user = await crud.find_existed_user(token_data.phone_number)
    if user is None:
        raise credentials_exception
    return schemas.UserListStatus(**user)


def get_current_active_user(
    current_user: schemas.UserListStatus = Depends(get_current_user),
):
    if not current_user.status:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
