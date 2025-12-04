from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from uuid import UUID
from datetime import datetime   
from sqlmodel import Session

from services import report_service
from app.db.session import get_session

router = APIRouter(prefix="/report", tags=["Report"])

@router.get("/org/{org_id}/user/{user_id}/generate")
async def generate_report(org_id : UUID, user_id : UUID, start_date : datetime, end_date : datetime, db : Session = Depends(get_session)):    
    """
    Generates a report of all activities for a given user and organization, 
    filtered by the given initial and end dates.

    Args:
        org_id (UUID): The id of the organization.
        user_id (UUID): The id of the user.
        start_date (datetime): The initial date for the filter.
        end_date (datetime): The end date for the filter.
        db (Session): The database session.

    Returns:
        StreamingResponse: A StreamingResponse containing the report in PDF format.
    """
    pdf_buffer = report_service.generate_report(org_id, user_id, start_date, end_date, db)

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=relatorio_tarefas.pdf"
        }
    )

