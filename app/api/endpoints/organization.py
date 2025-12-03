from fastapi import APIRouter, Depends
from sqlmodel import Session
from uuid import UUID

from app.schemas.user_schema import UserWithoutPassword
from app.schemas.organization_schema import OrganizationRead
from app.db.session import get_session
from app.crud import org_user_crud, organization_crud

router = APIRouter(prefix="/organization", tags=["Organization"])


@router.get('/{org_id}', response_model=OrganizationRead)
def get_organization(org_id : UUID, db : Session = Depends(get_session)):
    """
    Retrieves an organization by its id

    Args:
        org_id (UUID): The id of the organization to retrieve.

    Returns:
        OrganizationRead: The retrieved organization.
    """
    return organization_crud.get_organization_by_id(db, org_id)

@router.get("/{org_id}/supervisor", response_model=UserWithoutPassword)
def get_organization_supervisor(org_id : UUID, db : Session = Depends(get_session)):
    """
    Retrieves the supervisor associated with a given organization id.

    Args:
        org_id (UUID): The id of the organization to retrieve the supervisor for.

    Returns:
        Users: The supervisor associated with the given organization id.

    Raises:
        HTTPException: If the organization with the given id was not found.
    """
    return org_user_crud.get_supervisor_by_org_id(db, org_id)