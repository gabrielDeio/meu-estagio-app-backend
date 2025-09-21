from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.schemas.auth_schema import Token, AuthSchema
from app.db.session import get_session
from app.crud.auth_crud import authenticate

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=Token)
def login(form_data : AuthSchema, db : Session = Depends(get_session)) -> Token:
    jwt = authenticate(db, auth_in=form_data)

    return Token(access_token=jwt, token_type="Bearer")