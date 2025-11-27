from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.schemas.auth_schema import Token, AuthSchema, LoginResponseSchema
from app.db.session import get_session
from app.crud.auth_crud import authenticate

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=LoginResponseSchema)
def login(form_data : AuthSchema, db : Session = Depends(get_session)) -> Token:
    return authenticate(db, auth_in=form_data)