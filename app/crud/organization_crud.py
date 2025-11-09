from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select

from app.models.organization import Organization
from app.schemas.organization_schema import OrganizationCreate, OrganizationUpdate

def get_organization_by_id(db : Session, organization_id : UUID) -> Optional[Organization]:
    """
    Returns a Organization by an id
    """
    return db.exec(select(Organization).where(Organization.id == organization_id)).first()

def get_organization_by_cnpj(db : Session, cnpj : str) -> Optional[Organization]:
    """
    Returns a Organization by an cnpj
    """
    return db.exec(select(Organization).where(Organization.cnpj == cnpj)).first()

def get_organization_by_register_code(db : Session, code : str) -> Optional[Organization]:
    """
    Returns a Organization by an code
    """
    return db.exec(select(Organization).where(Organization.code == code)).first()

def get_all_oganizations(db : Session) -> List[Organization]:
    """
    Returns all Organizations stored in db
    """
    result =  db.exec(select(Organization)).all()

    return list(result)


def create_organization(db : Session, organization_in : OrganizationCreate) -> Organization:
    """
    Creates an Organization
    """
    organization_data = organization_in.model_dump()
    organization = Organization(**organization_data)

    db.add(organization)
    db.commit()
    db.refresh(organization)
    return organization

def update_organization(db : Session, organization : Organization, organization_in : OrganizationUpdate) -> Organization :
    """
    Updates an organization
    """
    for key, value in organization_in.model_dump(exclude_unset=True).items():
        setattr(organization, key, value)

    db.add(organization)
    db.commit()
    db.refresh(organization)
    return organization

def delete_organization(db : Session, organization : Organization):
    """
    Deletes an organization
    """
    db.delete(organization)
    db.commit()
