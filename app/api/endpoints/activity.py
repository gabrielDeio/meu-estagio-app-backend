from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from uuid import UUID
from typing import List

from app.models.activity import Activity
from app.schemas.activity_schema import ActivityCreate, ActivityUpdate
from app.db.session import get_session
from services import activity_service
from app.crud import activity_crud

router = APIRouter(prefix="/activity", tags=["Activity"])


@router.post("/", response_model=Activity, status_code=status.HTTP_201_CREATED)
def create_activity_endpoint(activity_in : ActivityCreate, db : Session = Depends(get_session)):
    """
    Creates a new Activity.

    Args:
        activity_in (ActivityCreate): The activity to be created.
        db (Session): The database session.

    Returns:
        Activity: The newly created activity.

    Raises:
        HTTPException: If the Activity with the given id was not found.
    """
    return activity_service.create_activity(activity_in, db)

@router.get("/{org_id}/user/{user_id}", response_model=List[Activity])
def get_user_activities_endpoint(org_id : UUID, user_id : UUID, db : Session = Depends(get_session)):
    """
    Retrieves all activities for a given user and organization.

    Args:
        org_id (UUID): The id of the organization.
        user_id (UUID): The id of the user.

    Returns:
        Activity: A list of all activities for the user and organization.
    """
    return activity_crud.get_user_org_activities(db=db, user_id=user_id, org_id=org_id)

@router.get("/{activity_id}", response_model=Activity)
def get_activity_endpoint(activity_id : UUID, db : Session = Depends(get_session)):
    """
    Retrieves an Activity by id.

    Args:
        activity_id (UUID): The id of the Activity to be retrieved.
        db (Session): The database session.

    Returns:
        Activity: The Activity with the given id.

    Raises:
        HTTPException: If the Activity with the given id was not found.
    """
    return activity_crud.get_activity(db, activity_id)

@router.patch("/{activity_id}", response_model=Activity)
def update_activity_endpoint(activity_id : UUID, activity_in : ActivityUpdate, db : Session = Depends(get_session)):
    """
    Updates an Activity.

    Args:
        activity_id (UUID): The id of the activity to be updated.
        activity_in (ActivityUpdate): The activity data to be updated.
        db (Session): The database session.

    Returns:
        Activity: The updated activity.

    Raises:
        HTTPException: If the Activity with the given id was not found.
    """
    return activity_service.update_activity(activity_id, activity_in, db)

@router.delete("/{activity_id}", response_model=Activity)
def delete_activity_endpoint(activity_id : UUID, db : Session = Depends(get_session)):
    """
    Deletes an Activity.

    Args:
        activity_id (UUID): The id of the activity to be deleted.
        db (Session): The database session.

    Returns:
        Activity: The deleted activity.

    Raises:
        HTTPException: If the Activity with the given id was not found.
    """
    return activity_service.delete_activity(activity_id, db)