from sqlmodel import Session, UUID
from fastapi import Depends, HTTPException, status

from app.models.activity import Activity
from app.schemas.activity_schema import ActivityCreate, ActivityUpdate
from app.db.session import get_session
from app.crud import activity_crud

def create_activity(activity_in : ActivityCreate, db : Session = Depends(get_session)) -> Activity :
    """
    Creates a new Activity.

    Args:
        activity_in (ActivityCreate): The activity data to be created.
        db (Session): The database session.

    Returns:
        Activity: The newly created activity.

    Raises:
        HTTPException: If the Activity with the given id was not found.
    """
    return activity_crud.create_activity(db, activity_in)

def update_activity(activity_id : UUID, activity_in : ActivityUpdate, db : Session = Depends(get_session)) -> Activity:
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

    activity = activity_crud.get_activity(db, activity_id)
    if not activity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activity was not found")

    return activity_crud.update_activity(db, activity_in, activity_id)


def delete_activity(activity_id : UUID, db : Session = Depends(get_session)):
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
    activity = activity_crud.get_activity(db, activity_id)
    if not activity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activity was not found")

    return activity_crud.delete_activity(db, activity_id)