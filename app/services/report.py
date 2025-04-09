from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import csv
import io
import json
from sqlalchemy import func, desc, and_, extract
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.models.user import User
from app.schemas.report import ReportType, ReportFormat, ReportFilters

def generate_sales_by_customer_report(db: Session, filters: ReportFilters) -> List[Dict[str, Any]]:
    """Generar reporte de ventas por cliente."""
    query = db.query(
        User.id.label("customer_id"),
        User.username.label("customer_name"),
        User.email.label("customer_email"),
        func.count(Order.id).label("order_count"),
        func.sum(Order.total_amount).label("total_spent")
    ).join(Order, Order.user_id == User.id)
    
    # Aplicar filtros
    if filters.start_date:
        query = query.filter(Order.created_at >= filters.start_date)
    if filters.end_date:
        query = query.filter(Order.created_at <= filters.end_date)
    if filters.customer_id:
        query = query.filter(User.id == filters.customer_id)
    
    result = query.group_by(User.id, User.username, User.email)\
        .order_by(func.sum(Order.total_amount).desc())\
        .limit(filters.limit)\
        .all()
    
    return [
        {
            "customer_id": r.customer_id,
            "customer_name": r.customer_name,
            "customer_email": r.customer_email,
            "order_count": r.order_count,
            "total_spent": float(r.total_spent) if r.total_spent else 0.0
        }
        for r in result
    ]

def generate_top_selling_products_report(db: Session, filters: ReportFilters) -> List[Dict[str, Any]]:
    """Generar reporte de productos más vendidos."""
    query = db.query(
        Product.id.label("product_id"),
        Product.name.label("product_name"),
        Product.category.label("category"),
        func.sum(OrderItem.quantity).label("total_quantity"),
        func.sum(OrderItem.quantity * OrderItem.unit_price).label("total_revenue")
    ).join(OrderItem, OrderItem.product_id == Product.id)\
    .join(Order, Order.id == OrderItem.order_id)
    
    # Aplicar filtros
    if filters.start_date:
        query = query.filter(Order.created_at >= filters.start_date)
    if filters.end_date:
        query = query.filter(Order.created_at <= filters.end_date)
    if filters.product_category:
        query = query.filter(Product.category == filters.product_category)
    
    result = query.group_by(Product.id, Product.name, Product.category)\
        .order_by(func.sum(OrderItem.quantity).desc())\
        .limit(filters.limit)\
        .all()
    
    return [
        {
            "product_id": r.product_id,
            "product_name": r.product_name,
            "category": r.category,
            "total_quantity": r.total_quantity,
            "total_revenue": float(r.total_revenue) if r.total_revenue else 0.0
        }
        for r in result
    ]

def generate_sales_by_period_report(db: Session, filters: ReportFilters) -> List[Dict[str, Any]]:
    """Generar reporte de ventas por período."""
    # Determinar período (diario, semanal, mensual) basado en el rango de fechas
    if not filters.start_date or not filters.end_date:
        # Por defecto, último mes
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
    else:
        start_date = filters.start_date
        end_date = filters.end_date
    
    date_diff = (end_date - start_date).days
    
    if date_diff <= 31:
        # Reporte diario
        query = db.query(
            func.date(Order.created_at).label("period"),
            func.count(Order.id).label("order_count"),
            func.sum(Order.total_amount).label("total_sales")
        )
        group_format = "day"
    elif date_diff <= 90:
        # Reporte semanal
        query = db.query(
            func.date_trunc('week', Order.created_at).label("period"),
            func.count(Order.id).label("order_count"),
            func.sum(Order.total_amount).label("total_sales")
        )
        group_format = "week"
    else:
        # Reporte mensual
        query = db.query(
            func.date_trunc('month', Order.created_at).label("period"),
            func.count(Order.id).label("order_count"),
            func.sum(Order.total_amount).label("total_sales")
        )
        group_format = "month"
    
    # Aplicar filtros de fecha
    query = query.filter(Order.created_at >= start_date, Order.created_at <= end_date)
    
    result = query.group_by("period").order_by("period").all()
    
    return [
        {
            "period": r.period.strftime('%Y-%m-%d') if group_format == "day" else
                     r.period.strftime('%Y-%m-%d') + " (Week)" if group_format == "week" else
                     r.period.strftime('%Y-%m'),
            "order_count": r.order_count,
            "total_sales": float(r.total_sales) if r.total_sales else 0.0
        }
        for r in result
    ]

def generate_inventory_status_report(db: Session, filters: ReportFilters) -> List[Dict[str, Any]]:
    """Generar reporte de estado del inventario."""
    query = db.query(
        Product.id.label("product_id"),
        Product.name.label("product_name"),
        Product.category.label("category"),
        Product.stock.label("current_stock"),
        Product.price.label("unit_price")
    )
    
    # Aplicar filtros
    if filters.product_category:
        query = query.filter(Product.category == filters.product_category)
    
    result = query.order_by(Product.stock).limit(filters.limit).all()
    
    return [
        {
            "product_id": r.product_id,
            "product_name": r.product_name,
            "category": r.category,
            "current_stock": r.current_stock,
            "unit_price": float(r.unit_price),
            "inventory_value": float(r.unit_price * r.current_stock)
        }
        for r in result
    ]

def generate_report(db: Session, report_type: ReportType, filters: ReportFilters) -> List[Dict[str, Any]]:
    """Generar reporte según su tipo."""
    if report_type == ReportType.SALES_BY_CUSTOMER:
        return generate_sales_by_customer_report(db, filters)
    elif report_type == ReportType.TOP_SELLING_PRODUCTS:
        return generate_top_selling_products_report(db, filters)
    elif report_type == ReportType.SALES_BY_PERIOD:
        return generate_sales_by_period_report(db, filters)
    elif report_type == ReportType.INVENTORY_STATUS:
        return generate_inventory_status_report(db, filters)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tipo de reporte no soportado: {report_type}"
        )

def format_report(data: List[Dict[str, Any]], format: ReportFormat) -> Any:
    """Formatear reporte según el formato solicitado."""
    if format == ReportFormat.JSON:
        return data
    elif format == ReportFormat.CSV:
        if not data:
            return ""
        
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
        return output.getvalue()
    else:
        # Para otros formatos (PDF, EXCEL) se necesitaría implementar la lógica
        # usando bibliotecas adicionales
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail=f"Formato de reporte no implementado: {format}"
        ) 