from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class ReportType(str, Enum):
    SALES_BY_CUSTOMER = "sales_by_customer"
    TOP_SELLING_PRODUCTS = "top_selling_products"
    SALES_BY_PERIOD = "sales_by_period"
    INVENTORY_STATUS = "inventory_status"

class ReportFormat(str, Enum):
    JSON = "json"
    CSV = "csv"
    PDF = "pdf"
    EXCEL = "excel"

# Esquema para solicitar un reporte
class ReportRequest(BaseModel):
    report_type: ReportType
    format: ReportFormat = ReportFormat.JSON
    params: Dict[str, Any] = {}

# Esquema para filtros de reportes
class ReportFilters(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    customer_id: Optional[int] = None
    product_category: Optional[str] = None
    limit: Optional[int] = Field(10, ge=1, le=100)

# Item básico para reportes
class ReportItem(BaseModel):
    id: int
    label: str
    value: float

# Respuesta de reporte
class ReportResponse(BaseModel):
    report_type: ReportType
    generated_at: datetime
    data: List[Dict[str, Any]]
    summary: Dict[str, Any] = {} 