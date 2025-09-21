from sqlmodel import Session
from fastapi import status, HTTPException


from app.schemas.auth_schema import AuthSchema
from app.crud.user_crud import get_user_by_email
from app.utils.hash import verify_password
from app.core.security import generate_access_toke


def authenticate(db : Session, auth_in : AuthSchema) -> str:
    user = get_user_by_email(db, user_email=auth_in.email, user_type=auth_in.type)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")
    
    equal = verify_password(password=auth_in.password, hashed_password=user.password)

    if not equal:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    jwt = generate_access_toke(data={"sub" : str(user.id)})

    return jwt

