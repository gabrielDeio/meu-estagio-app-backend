import io
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from sqlmodel import Session, UUID
from fastapi import Depends
from datetime import datetime
from reportlab.lib import pagesizes

from app.db.session import get_session
from app.crud.activity_crud import get_user_org_activities
from app.models.activity import ActitivityStatus


def generate_report(org_id : UUID, user_id : UUID, initial_date : datetime, end_date : datetime, db : Session = Depends(get_session)):
    activities = get_user_org_activities(db=db, user_id=user_id, org_id=org_id, start_date=initial_date, end_date=end_date)

    buffer = io.BytesIO()
    
    doc = SimpleDocTemplate(buffer, pagesize=pagesizes.A4)
    elements = []
    styles = getSampleStyleSheet()
    
    elements.append(Paragraph("Relatório de Atividades/Tarefas", styles['Title']))
    elements.append(Paragraph(f"Total de Registros: {len(activities)}", styles['Normal']))
    
    data_table = [
        ['Nome', 'Status','Descrição', 'Início', 'Fim', 'Criado em']
    ]


    for activity in activities:
        status_to_save = ''

        if activity.status == ActitivityStatus.PENDING:
            status_to_save = 'Pendente'

        elif activity.status == ActitivityStatus.APPROVED:
            status_to_save = 'Aprovado'

        elif activity.status == ActitivityStatus.REJECTED:
            status_to_save = 'Rejeitado'

        data_table.append([
            activity.name,
            status_to_save,
            activity.description,
            activity.start_time.strftime('%d/%m/%Y %H:%M'),
            activity.end_time.strftime('%d/%m/%Y %H:%M'),
            activity.created_at.strftime('%d/%m/%Y %H:%M'),
        ])

    t = Table(data_table)
    
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey), 
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke), 
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige), 
        ('GRID', (0, 0), (-1, -1), 1, colors.black) 
    ]))
    
    elements.append(t)
    
    
    doc.build(elements)
    
    buffer.seek(0)
    return buffer
