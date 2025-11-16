from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from uuid import UUID

from app.models.users import Users
from app.schemas.user_schema import UserCreate, UserUpdate, UserRead
from app.db.session import get_session
from app.crud import user_crud
from services import user_service

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=Users, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(user_in : UserCreate, db : Session = Depends(get_session)):
    """
    Endpoint to create a new user.

    Args:
        user_in (UserCreate): The user data to be created.

    Returns:
        User: The newly created user.

    Raises:
        HTTPException: If the user with the given email already exists.
    """
    return user_service.register_user(user_in, db)


@router.get("/", response_model=List[UserRead])
def get_users_endpoint(db : Session = Depends(get_session)):
    """
    Endpoint to get all users.
    
    Returns:
        List[UserRead]: A list of all users.
    """
    return user_crud.get_all_users(db)

@router.get("/{user_id}", response_model=UserRead)
def get_user_endpoint(user_id : UUID, db : Session = Depends(get_session)):
    """
    Endpoint to get a user by id.

    Args:
        user_id (UUID): The id of the user to be retrieved.

    Returns:
        UserRead: The user with the given id.

    Raises:
        HTTPException: If the user with the given id was not found.
    """
    user = user_crud.get_user_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")
    
    return user

@router.patch("/{user_id}", response_model=UserRead)
def update_user_endpoint(user_id : UUID, user_in : UserUpdate, db : Session = Depends(get_session)):
    """
    Endpoint to update a user by id.

    Args:
        user_id (UUID): The id of the user to be updated.
        user_in (UserUpdate): The user data to be updated.

    Returns:
        UserRead: The updated user.

    Raises:
        HTTPException: If the user with the given id was not found.
    """
    user = user_crud.get_user_by_id(db, user_id, user_type=user_in.type)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")
    
    return user_crud.update_user(db, user, user_in)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_endpoint(user_id : UUID, db : Session = Depends(get_session)):
    """
    Endpoint to delete a user by id.

    Args:
        user_id (UUID): The id of the user to be deleted.

    Returns:
        None

    Raises:
        HTTPException: If the user with the given id was not found.
    """
    return user_crud.delete_user(db, user_id) 
