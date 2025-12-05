import io
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, LongTable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from sqlmodel import Session, UUID
from fastapi import Depends
from datetime import datetime
from reportlab.lib import pagesizes

from app.db.session import get_session
from app.crud.activity_crud import get_user_org_activities
from app.models.activity import ActitivityStatus


def generate_report(org_id: UUID, user_id: UUID, initial_date: datetime, end_date: datetime, db: Session = Depends(get_session)):
    activities = get_user_org_activities(
        db=db, user_id=user_id, org_id=org_id,
        start_date=initial_date, end_date=end_date
    )

    buffer = io.BytesIO()
    
    doc = SimpleDocTemplate(buffer, pagesize=pagesizes.A4,
                            leftMargin=30, rightMargin=30, topMargin=30, bottomMargin=30)
    elements = []
    styles = getSampleStyleSheet()

    normal_style = ParagraphStyle(
        'normal_small',
        parent=styles['Normal'],
        fontSize=8,
        leading=10,
        wordWrap='CJK'  
    )
    
    elements.append(Paragraph("Relatório de Atividades/Tarefas", styles['Title']))
    elements.append(Paragraph(f"Total de Registros: {len(activities)}", styles['Normal']))
    
    data_table = [
        ['Nome', 'Status','Descrição', 'Início', 'Fim', 'Criado em']
    ]

    for activity in activities:
        if activity.status == ActitivityStatus.PENDING:
            status_to_save = 'Pendente'
        elif activity.status == ActitivityStatus.APPROVED:
            status_to_save = 'Aprovado'
        else:
            status_to_save = 'Rejeitado'

        data_table.append([
            Paragraph(activity.name or '', normal_style),
            Paragraph(status_to_save, normal_style),
            Paragraph(activity.description or '', normal_style),
            Paragraph(activity.start_time.strftime('%d/%m/%Y %H:%M'), normal_style),
            Paragraph(activity.end_time.strftime('%d/%m/%Y %H:%M'), normal_style),
            Paragraph(activity.created_at.strftime('%d/%m/%Y %H:%M'), normal_style),
        ])

    col_widths = [120, 60, 200, 60, 60, 35]  

    t = LongTable(data_table, colWidths=col_widths, repeatRows=1)
    
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey), 
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke), 
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige), 
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('WORDWRAP', (0,0), (-1,-1), 'CJK'),
    ]))
    
    elements.append(t)
    
    doc.build(elements)
    
    buffer.seek(0)
    return buffer

