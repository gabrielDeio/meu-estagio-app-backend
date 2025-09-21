from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from uuid import UUID

from app.models.user import User
from app.schemas.user_schema import UserCreate, UserUpdate, UserRead
from app.db.session import get_session
from app.crud import user_crud

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(user_in : UserCreate, db : Session = Depends(get_session)):
    """
    Endpoint to create a new User.
    """
    existing_user = user_crud.get_user_by_email(db, user_email=user_in.email, user_type=user_in.type)
    if existing_user:
        raise HTTPException( status_code=status.HTTP_409_CONFLICT, detail="User with this email already exists")
    
    return user_crud.create_user(db, user_in=user_in)


@router.get("/", response_model=List[UserRead])
def get_users_endpoint(db : Session = Depends(get_session)):
    """
    Enpoint to get all Users stored in dabatase
    """
    return user_crud.get_all_users(db)

@router.get("/{user_id}", response_model=UserRead)
def get_user_endpoint(user_id : UUID, db : Session = Depends(get_session)):
    """
    Endpoint to get a specific user by his id
    """
    user = user_crud.get_user_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")
    
    return user

@router.patch("/{user_id}", response_model=UserRead)
def update_user_endpoint(user_id : UUID, user_in : UserUpdate, db : Session = Depends(get_session)):
    """
    Endpoint to update a user
    """
    user = user_crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")
    
    return user_crud.update_user(db, user, user_in)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_endpoint(user_id : UUID, db : Session = Depends(get_session)):
    """
    Endpoint to delete a User
    """
    user = user_crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")

    user_crud.delete_user(db, user)
    return 
