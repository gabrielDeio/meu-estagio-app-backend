from jose import jwt
from typing import Optional
from datetime import timedelta, datetime, timezone

from app.core.config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ENCODE_ALGORITHM


def generate_access_toke(data : dict, expires_delta : Optional[timedelta] = None) -> str:
    """
    Function to generate jwt access token
    """
    to_encode = data.copy()

    if SECRET_KEY is None:
        raise ValueError("SECRET_KEY env is not set")
    if ENCODE_ALGORITHM is None:
        raise ValueError("ALGORITHM env is not set")

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        if ACCESS_TOKEN_EXPIRE_MINUTES is None:
            raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES env is not defined")
        
        expire = datetime.now(timezone.utc) + timedelta(minutes= int(ACCESS_TOKEN_EXPIRE_MINUTES))

    to_encode.update({"exp" : expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ENCODE_ALGORITHM)
    return encoded_jwt
         
