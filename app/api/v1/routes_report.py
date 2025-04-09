from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.db.session import get_db
from app.models.user import User
from app.core.security import get_current_active_user, get_current_user_with_permissions
from app.services import report as report_service
from app.schemas.report import ReportType, ReportFormat, ReportRequest, ReportFilters, ReportResponse
from datetime import datetime

router = APIRouter()

@router.post("/generate", response_model=ReportResponse)
def generate_report(
    request: ReportRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_with_permissions(["admin"]))
):
    """
    Generar un reporte según el tipo y parámetros especificados.
    Solo administradores pueden generar reportes.
    """
    # Extraer filtros de los parámetros
    filters = ReportFilters(**request.params) if request.params else ReportFilters()
    
    # Generar datos del reporte
    data = report_service.generate_report(db, report_type=request.report_type, filters=filters)
    
    # Construir respuesta
    response = ReportResponse(
        report_type=request.report_type,
        generated_at=datetime.now(),
        data=data
    )
    
    # Agregar resumen si hay datos
    if data:
        if request.report_type == ReportType.SALES_BY_CUSTOMER:
            response.summary = {
                "total_customers": len(data),
                "total_orders": sum(item["order_count"] for item in data),
                "total_revenue": sum(item["total_spent"] for item in data)
            }
        elif request.report_type == ReportType.TOP_SELLING_PRODUCTS:
            response.summary = {
                "total_products": len(data),
                "total_quantity": sum(item["total_quantity"] for item in data),
                "total_revenue": sum(item["total_revenue"] for item in data)
            }
        elif request.report_type == ReportType.SALES_BY_PERIOD:
            response.summary = {
                "periods": len(data),
                "total_orders": sum(item["order_count"] for item in data),
                "total_sales": sum(item["total_sales"] for item in data)
            }
        elif request.report_type == ReportType.INVENTORY_STATUS:
            response.summary = {
                "total_products": len(data),
                "total_stock": sum(item["current_stock"] for item in data),
                "total_value": sum(item["inventory_value"] for item in data)
            }
    
    return response

@router.post("/export")
def export_report(
    request: ReportRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_with_permissions(["admin"]))
):
    """
    Exportar un reporte en el formato especificado.
    Solo administradores pueden exportar reportes.
    """
    # Extraer filtros de los parámetros
    filters = ReportFilters(**request.params) if request.params else ReportFilters()
    
    # Generar datos del reporte
    data = report_service.generate_report(db, report_type=request.report_type, filters=filters)
    
    # Formatear datos según el formato solicitado
    try:
        formatted_data = report_service.format_report(data, format=request.format)
    except HTTPException as e:
        raise e
    
    # Configurar la respuesta según el formato
    if request.format == ReportFormat.JSON:
        return formatted_data
    elif request.format == ReportFormat.CSV:
        filename = f"{request.report_type.value}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        return Response(
            content=formatted_data,
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail=f"Formato de reporte no implementado: {request.format}"
        ) 