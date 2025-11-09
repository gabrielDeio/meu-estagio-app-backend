from sqlmodel import Session, UUID
from fastapi import Depends, HTTPException, status

from app.schemas.organization_schema import OrganizationCreate, OrganizationUpdate
from app.db.session import get_session
from app.crud import organization_crud

def create_organization(organization_id : OrganizationCreate, db : Session = Depends(get_session)):
    """
    Logic to create an organization
    """
    existing_org = organization_crud.get_organization_by_cnpj(db, cnpj=organization_id.cnpj)

    if existing_org:
        raise HTTPException( status_code=status.HTTP_409_CONFLICT, detail="Organization with this cnpj already exists")
    
    return organization_crud.create_organization(db, organization_in=organization_id)

def update_organization(organization_id : UUID, organization_in : OrganizationUpdate, db : Session = Depends(get_session)):
    """
    Logic to update an organization
    """
    existing_org = organization_crud.get_organization_by_id(db, organization_id=organization_id)

    if not existing_org:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail="Organization was not found")
    
    return organization_crud.update_organization(db, organization=existing_org, organization_in=organization_in)

def delete_organization(organization_id : UUID, db : Session = Depends(get_session)):
    """
    Logic to delete an organization
    """
    existing_org = organization_crud.get_organization_by_id(db, organization_id=organization_id)

    if not existing_org:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail="Organization was not found")
    
    return organization_crud.delete_organization(db, organization=existing_org)
