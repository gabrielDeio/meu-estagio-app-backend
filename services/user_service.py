from fastapi import Depends, HTTPException, status
from sqlmodel import Session, UUID

from app.crud import user_crud
from app.crud import organization_crud
from app.crud import org_user_crud
from app.db.session import get_session
from app.schemas.user_schema import UserCreate, UserTypeEnum
from app.models.org_user import OrgUser, StatusEnum
from app.models.users import Users
from app.models.organization import Organization
from app.utils import organization_code

def register_user(user_in : UserCreate, db : Session = Depends(get_session)):
    """
    Registers a new user.

    Args:
        user_in (UserCreate): The user data to be registered.
        db (Session): The database session.

    Returns:
        User: The newly registered user.

    Raises:
        HTTPException: If the user with the given email already exists.
    """
    existing_user = user_crud.get_user_by_email(db, user_in.email, user_in.type)

    if existing_user :
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with this email already exists")
    
    if user_in.type == UserTypeEnum.STUDENT:
        return register_student(user_in, db)
    
    if user_in.type == UserTypeEnum.SUPERVISOR:
        return register_supervisor(user_in, db)



def register_student(user_in : UserCreate, db : Session = Depends(get_session)) -> Users:
    """
    Registers a new student user.

    Args:
        user_in (UserCreate): The user data to be registered.
        db (Session): The database session.

    Returns:
        User: The newly registered user.

    Raises:
        HTTPException: If the company code is not provided or if the organization with the given code was not found.
    """
    if not user_in.code:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Company code is required")

    existing_org = organization_crud.get_organization_by_register_code(db, code=user_in.code)

    if not existing_org:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization was not found")
    
    user_created = user_crud.create_user(db, user_in=user_in)
    
    org_user_relation = OrgUser(org_id=existing_org.id, user_id=user_created.id, type=UserTypeEnum.STUDENT, status=StatusEnum.ACTIVE)

    org_user_crud.create_org_user_relation(db, org_user_in=org_user_relation)

    return user_created

def register_supervisor(user_in : UserCreate, db : Session = Depends(get_session)) -> Users:
    """
    Registers a new supervisor user.

    Args:
        user_in (UserCreate): The user data to be registered.
        db (Session): The database session.

    Returns:
        User: The newly registered user.

    Raises:
        HTTPException: If the cnpj is not provided or if the organization with the given cnpj already exists.
    """
    if not user_in.cnpj:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="CNPJ is required")
    
    existing_org = organization_crud.get_organization_by_cnpj(db, cnpj=user_in.cnpj)

    if existing_org:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Organization with this cnpj already exists")
    
    organization = Organization(name=user_in.company_name, supervisor_max_amount=user_in.supervisor_max_amount, cnpj=user_in.cnpj, code=organization_code.generate())
    
    created_org = organization_crud.create_organization(db, organization_in=organization)
    
    user_created = user_crud.create_user(db, user_in=user_in)

    org_user_relation = OrgUser(org_id=created_org.id, user_id=user_created.id, type=UserTypeEnum.SUPERVISOR, status=StatusEnum.ACTIVE)

    org_user_crud.create_org_user_relation(db, org_user_in=org_user_relation)

    return user_created

def delete_student(user_id : UUID, db : Session = Depends(get_session)):
    """
    Deletes a student user by id. This action also delete all org_user relations for this user.

    Args:
        user_id (UUID): The id of the user to be deleted.
        db (Session): The database session.

    Returns:
        None

    Raises:
        HTTPException: If the user with the given id was not found.
    """
    user = user_crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")
    
    org_user_crud.delete_all_user_relation(db, user_id)

    user_crud.delete_user(db, user)

    return