from sqlmodel import Session
from fastapi import status, HTTPException


from app.schemas.auth_schema import AuthSchema, LoginResponseSchema, UserResponseSchema
from app.crud.user_crud import get_user_by_email
from app.crud.org_user_crud import get_org_by_user_id
from app.utils.hash import verify_password
from app.core.security import generate_access_token


def authenticate(db : Session, auth_in : AuthSchema) -> str:
    """
    Authenticates a user and returns a JWT token.

    Args:
        db (Session): The database session.
        auth_in (AuthSchema): The user data to be authenticated.

    Returns:
        str: A JWT token containing the user's id and type.

    Raises:
        HTTPException: If the user was not found or the credentials are invalid.
    """
    user = get_user_by_email(db, user_email=auth_in.email, user_type=auth_in.type)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")
    
    equal = verify_password(password=auth_in.password, hashed_password=user.password)

    if not equal:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    org_user = get_org_by_user_id(db, user_id=user.id)

    jwt = generate_access_token(data={"sub" : str(user.id), "type" : user.type})

    userData = UserResponseSchema(id = user.id, name = user.name, email=user.email, type=user.type)


    return LoginResponseSchema(access_token=jwt, token_type="Bearer", user=userData, org_id=org_user.org_id)

