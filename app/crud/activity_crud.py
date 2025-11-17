from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select

from app.models.activity import Activity
from app.schemas.activity_schema import ActivityCreate, ActivityUpdate

def get_activity(db : Session, activity_id : UUID) -> Activity:
    """
    Retrieves an Activity by id.

    Args:
        db (Session): A database session.
        activity_id (UUID): The id of the Activity to be retrieved.

    Returns:
        Activity: The Activity with the given id.

    Raises:
        HTTPException: If the Activity with the given id was not found.
    """
    return db.exec(select(Activity).where(Activity.id == activity_id)).first()

def get_org_activities(db : Session, org_id : UUID) -> List[Activity]:
    """
    Retrieves all activities for an organization.

    Args:
        db (Session): A database session.
        org_id (UUID): The id of the organization.

    Returns:
        List[Activity]: A list of all activities for the organization.
    """
    return db.exec(select(Activity).where(Activity.organization_id == org_id)).all()

def get_user_org_activities(db : Session, user_id : UUID, org_id : UUID) -> List[Activity]:
    """
    Retrieves all activities for a given user and organization.

    Args:
        db (Session): A database session.
        user_id (UUID): The id of the user.
        org_id (UUID): The id of the organization.

    Returns:
        List[activity]: A list of all activities for the user and organization.
    """
    statement = select(Activity).where(
        Activity.organization_id == org_id,
        Activity.user_id == user_id
    )
    
    return db.exec(statement).all()

def create_activity(db : Session, activity_in : ActivityCreate, activity_id : UUID) -> Activity:
    """
    Creates a new Activity.

    Args:
        db (Session): A database session.
        activity_in (ActivityCreate): The activity to be created.

    Returns:
        Activity: The newly created activity.
    """
    activity_data = activity_in.model_dump()
    activity = Activity(**activity_data)
    db.add(activity)
    db.commit()
    db.refresh(activity)

    return activity

def update_activity(db : Session, activity_in : ActivityUpdate):
    """
    Updates an Activity.

    Args:
        db (Session): A database session.
        activity_in (ActivityUpdate): The activity to be updated.

    Returns:
        Activity: The updated activity.

    Raises:
        HTTPException: If the Activity with the given id was not found.
    """
    activity = get_activity(db, activity_in.id)
    for key, value in activity_in.model_dump(exclude_unset=True).items():
        setattr(activity, key, value)

    db.add(activity)
    db.commit()
    db.refresh(activity)

    return activity

def delete_activity(db : Session, activity_id : UUID):
    """
    Deletes an Activity.

    Args:
        db (Session): A database session.
        activity_id (UUID): The id of the activity to be deleted.

    Returns:
        Activity: The deleted activity.

    Raises:
        HTTPException: If the Activity with the given id was not found.
    """
    activity = get_activity(db, activity_id)
    db.delete(activity)
    db.commit()