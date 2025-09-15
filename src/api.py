from fastapi import APIRouter, HTTPException, Query
from typing import List

from src.data_processor import (
    EQUIPMENT_DATA,
    MAINTENANCE_DATA,
    extract_equipment_entities,
    extract_locations,
    extract_maintenance_types,
)
from src.models import Equipment, MaintenanceLog

# Create a router for API endpoints
router = APIRouter(prefix="/api", tags=["Utility Knowledge API"])

# Endpoints
@router.get("/equipment", response_model=List[Equipment])
def get_all_equipment():
    """Return all equipment entries."""
    if not EQUIPMENT_DATA:
        raise HTTPException(status_code=404, detail="No equipment data available.")
    return EQUIPMENT_DATA


@router.get("/maintenance", response_model=List[MaintenanceLog])
def get_all_maintenance():
    """Return all maintenance log entries."""
    if not MAINTENANCE_DATA:
        raise HTTPException(status_code=404, detail="No maintenance data available.")
    return MAINTENANCE_DATA


@router.get("/search", response_model=dict)
def search_entities(query: str = Query(..., description="Search term for equipment, location, or maintenance type")):
    """
    Search across:
    - Equipment: id, model, type, location
    - Maintenance: equipment_id or maintenance_type
    """
    q = query.strip().lower()

    # Match equipment on ID, model, type, or location
    equipment_matches = [
        e for e in EQUIPMENT_DATA
        if q in e.equipment_id.lower()
        or q in e.model.lower()
        or q in e.equipment_type.lower()
        or q in e.location.lower()
    ]

    # Match maintenance logs on equipment_id or maintenance_type
    maintenance_matches = [
        m for m in MAINTENANCE_DATA
        if q in m.equipment_id.lower()
        or q in m.maintenance_type.lower()
    ]

    if not equipment_matches and not maintenance_matches:
        raise HTTPException(status_code=404, detail="No matches found.")

    return {
        "query": query,
        "equipment_matches": equipment_matches,
        "maintenance_matches": maintenance_matches,
    }




@router.get("/info", response_model=dict)
def get_info():
    """Return metadata: unique equipment models, locations, and maintenance types."""
    return {
        "unique_equipment_models": extract_equipment_entities(),
        "unique_locations": extract_locations(),
        "maintenance_types": extract_maintenance_types(),
    }
