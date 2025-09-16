"""
api.py

Contains FastAPI route definitions for exposing equipment and maintenance data
via REST API endpoints (list, search, metadata, and export).
"""


from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse, StreamingResponse
from typing import List
from datetime import date
import io
import csv

from src.data_processor import (
    EQUIPMENT_DATA,
    MAINTENANCE_DATA,
    extract_equipment_entities,
    extract_locations,
    extract_maintenance_types,
)
from src.models import Equipment, MaintenanceLog

# Router for API endpoints
router = APIRouter(prefix="/api", tags=["Utility Knowledge API"])

# Endpoints
@router.get("/equipment", response_model=List[Equipment])
def get_all_equipment():
    """
    Return all equipment entries.
    """
    if not EQUIPMENT_DATA:
        raise HTTPException(status_code=404, detail="No equipment data available.")
    return EQUIPMENT_DATA


@router.get("/maintenance", response_model=List[MaintenanceLog])
def get_all_maintenance():
    """
    Return all maintenance log entries.
    """
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
    """
    Return metadata: unique equipment models, locations, and maintenance types.
    """
    return {
        "unique_equipment_models": extract_equipment_entities(),
        "unique_locations": extract_locations(),
        "maintenance_types": extract_maintenance_types(),
    }


@router.get("/export")
def export_data(format: str = Query("json", description="Export format: json or csv")):
    """
    Export combined equipment and maintenance data.
    """
    combined = []

    for eq in EQUIPMENT_DATA:
        logs = [m for m in MAINTENANCE_DATA if m.equipment_id == eq.equipment_id]
        if logs:
            for m in logs:
                # Build the record
                record = {
                    "equipment_id": eq.equipment_id,
                    "equipment_type": eq.equipment_type,
                    "location": eq.location,
                    "manufacturer": eq.manufacturer,
                    "model": eq.model,
                    "installation_date": eq.installation_date,
                    "status": eq.status,
                    "last_maintenance": eq.last_maintenance,
                    "log_id": m.log_id,
                    "maintenance_type": m.maintenance_type,
                    "maintenance_date": m.maintenance_date,
                    "technician": m.technician,
                    "description": m.description,
                    "maintenance_status": m.status,
                    "next_scheduled": m.next_scheduled,
                    "parts_used": m.parts_used,
                    "cost": m.cost,
                }

                # Convert any date values to strings inline
                for key, val in record.items():
                    if isinstance(val, date):
                        record[key] = val.isoformat()

                combined.append(record)

    if format == "json":
        return JSONResponse(content=combined)

    elif format == "csv":
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=combined[0].keys())
        writer.writeheader()
        writer.writerows(combined)
        output.seek(0)
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=export.csv"},
        )

    else:
        raise HTTPException(status_code=400, detail="Invalid format. Use 'json' or 'csv'.")
