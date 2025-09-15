from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class Equipment(BaseModel):
    """Data model for an piece of equipment."""
    equipment_id: str
    equipment_type: str
    location: str
    manufacturer: str
    model: str
    installation_date: date
    status: str
    last_maintenance: date

class MaintenanceLog(BaseModel):
    """Data model for a maintenance log entry."""
    log_id: str
    equipment_id: str
    maintenance_type: str
    maintenance_date: date = Field(..., alias="date")
    technician: str
    description: str
    status: str
    next_scheduled: Optional[date] = None
    parts_used: Optional[list[str]] = None
    cost: float