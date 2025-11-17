from jose import jwt, JWTError
from typing import Optional, List
from datetime import timedelta, datetime, timezone
from fastapi import Header, HTTPException, status, Cookie, Depends
from sqlmodel import Session

from app.core.config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ENCODE_ALGORITHM
from app.models.users import Users
from app.crud import user_crud
from app.db.session import get_session


CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"}, 
)

def generate_access_token(data : dict, expires_delta : Optional[timedelta] = None) -> str:
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
         
def _validate_token_and_get_user(db: Session, token: str) -> Users:
    """
    Validate a jwt token and return the corresponding user object.

    :param db: The database session.
    :param token: The jwt token to validate.
    :return: The user object if the token is valid, or raise an HTTPException if invalid.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ENCODE_ALGORITHM])
        user_id: str = payload.get("sub")
        type : str = payload.get("type")
        
        if user_id is None:
            raise CREDENTIALS_EXCEPTION
        
        user = user_crud.get_user_by_id(db, user_id=user_id, user_type=type)
        if user is None:
            raise CREDENTIALS_EXCEPTION
            
        return user
        
    except JWTError:
        raise CREDENTIALS_EXCEPTION


def get_current_user_priority(
    db: Session = Depends(get_session), 
    session_token: Optional[str] = Cookie(default=None),
    authorization: Optional[str] = Header(default=None, alias="Authorization"),
) -> Users:
    
    """
    Return the user object associated with the session token or authorization header.

    If neither session token nor authorization header is provided, raise an HTTPException.

    :param db: The database session.
    :param session_token: The session token to validate.
    :param authorization: The authorization header to validate.
    :return: The user object if the session token or authorization header is valid, or raise an HTTPException if invalid.
    """
    if session_token:
        try:
            return _validate_token_and_get_user(db, session_token)
        except HTTPException:
            pass
    
    if authorization:
        scheme, _, token = authorization.partition(" ")

        if scheme.lower() == "bearer" and token:
            try:
                return _validate_token_and_get_user(db, token)
            except HTTPException:
                 pass

    raise CREDENTIALS_EXCEPTION


def RoleGuard(required_role: str):
    """
    Guard that checks if the user has a specific role.
    
    This guard depends on the get_current_user_priority guard, which validates the user's session token or authorization header.
    If the user is valid, this guard checks if the user has the required role.
    If the user does not have the required role, an HTTPException is raised with a status code of 403 and a detail message indicating that the user does not have the required role to complete the action.
    """
    def role_checker(current_user: Users = Depends(get_current_user_priority)):
        user_type = current_user.type 
        
        if user_type != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User does not have the required role to complete this action",
            )
        
        return current_user

    return role_checker