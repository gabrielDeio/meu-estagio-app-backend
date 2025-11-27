from sqlmodel import Session, UUID, delete, select

from app.schemas.org_user_schema import OrgUserCreate, OrgUserUpdate
from app.models.org_user import OrgUser, StatusEnum

def create_org_user_relation(db : Session, org_user_in : OrgUserCreate) -> OrgUser:
    
    """
    Creates a new org_user relation.

    Args:
        db (Session): The database session.
        org_user_in (OrgUserCreate): The org_user data to be created.

    Returns:
        OrgUser: The newly created org_user relation.
    """
    org_user_data = org_user_in.model_dump()
    org_user = OrgUser(**org_user_data)
    org_user.status = StatusEnum.ACTIVE

    db.add(org_user)
    db.commit()
    db.refresh(org_user)
    return org_user

def update_org_user_relation(db : Session, org_user : OrgUser, org_user_in : OrgUserUpdate) -> OrgUser:
    """
    Updates an existing org_user relation.

    Args:
        db (Session): The database session.
        org_user (OrgUser): The org_user relation to be updated.
        org_user_in (OrgUserUpdate): The org_user data to be updated.

    Returns:
        OrgUser: The updated org_user relation.
    """
    for key, value in org_user_in.model_dump(exclude_unset=True).items():
        setattr(org_user, key, value)

    db.add(org_user)
    db.commit()
    db.refresh(org_user)
    return org_user

def delete_org_user_relation(db : Session, org_user : OrgUser):
    """
    Deletes an existing org_user relation.

    Args:
        db (Session): The database session.
        org_user (OrgUser): The org_user relation to be deleted.

    Returns:
        None
    """
    db.delete(org_user)
    db.commit()

def delete_all_user_relation(db : Session, user_id : UUID):
    """
    Deletes all org_user relations for a given user id.

    Args:
        db (Session): The database session.
        user_id (UUID): The id of the user to delete relations for.

    Returns:
        None
    """
    db.exec(delete(OrgUser).where(OrgUser.user_id == user_id))
    db.commit()

    return

def get_org_by_user_id(db : Session, user_id : UUID):
    return db.exec(select(OrgUser).where(OrgUser.user_id == user_id)).first()
