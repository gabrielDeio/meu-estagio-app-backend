from sqlmodel import Session, UUID, delete, select
from sqlalchemy import text

from app.schemas.org_user_schema import OrgUserCreate, OrgUserUpdate
from app.models.org_user import OrgUser, StatusEnum
from app.models.users import Users

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
    """
    Retrieves the organization associated with a given user id.

    Args:
        db (Session): The database session.
        user_id (UUID): The id of the user to retrieve the organization for.

    Returns:
        OrgUser: The org_user relation associated with the given user id.
    """
    return db.exec(select(OrgUser).where(OrgUser.user_id == user_id)).first()

def get_supervisor_by_org_id(db: Session, org_id: UUID):
    """
    Retrieves the supervisor associated with a given organization id.

    Args:
        db (Session): The database session.
        org_id (UUID): The id of the organization to retrieve the supervisor for.

    Returns:
        Tuple: A tuple containing the id, name, surname, email and type of the supervisor associated with the given organization id.
    """
    stmt = (
        text("""
            select u.id, u.name, u.surname, u.email, u.type 
            from core.org_user ou
            join core.users u on u.id = ou.user_id
            where ou.org_id = :org_id and ou.type = 'SUPERVISOR'
        """)
        .bindparams(org_id=org_id)
    )

    result = db.exec(stmt).first()

    return result


def get_students_organization(db : Session, org_id : UUID):
    """
    Retrieves all users associated with a given organization id.

    Args:
        db (Session): The database session.
        org_id (UUID): The id of the organization to retrieve the users for.

    Returns:
        List[OrgUser]: A list of org_user relations associated with the given organization id.
    """
    
    stmt = (
        text("""
            select u.id, u.name, u.surname, u.email, u.type 
            from core.org_user ou
            join core.users u on u.id = ou.user_id
            where ou.org_id = :org_id and ou.type = 'STUDENT'
        """)
        .bindparams(org_id=org_id)
    )

    result = db.exec(stmt).all()

    return result
