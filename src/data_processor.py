"""
data_processor.py

Handles loading, cleaning, and transforming CSV and JSON data into validated
Pydantic models. Also provides helper functions for extracting unique entities.
"""


import pandas as pd
import json
from pathlib import Path
from typing import List
from src.models import Equipment, MaintenanceLog

# File Paths
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
EQUIPMENT_FILE = DATA_DIR / "equipment_inventory.csv"
MAINTENANCE_FILE = DATA_DIR / "maintenance_logs.json"

# Load Functions
def load_equipment(path: Path) -> List[Equipment]:
    """
    Reads equipment CSV, normalize dates, and return validated Equipment objects.
    """
    df = pd.read_csv(path)

    # Rename columns to match model fields: optional
    df = df.rename(columns={"installed_on": "installation_date"})

    # Normalize date fields
    for col in ["installation_date", "last_maintenance"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
            df[col] = pd.to_datetime(df[col], errors="coerce").dt.date

    # Replace NaN with None for all fields
    df = df.where(pd.notna(df), None)

    rows: list[dict] = df.to_dict(orient="records")
    return [Equipment(**row) for row in rows]


def load_maintenance(path: Path) -> List[MaintenanceLog]:
    """
    Read maintenance JSON, normalize dates, handle null values, 
    and return validated MaintenanceLog objects.
    """
    with open(path, "r") as f:
        data = json.load(f)

    for entry in data:
        # Handle date field
        if "date" in entry:
            if entry["date"]:
                entry["date"] = pd.to_datetime(entry["date"], errors="coerce")
                entry["date"] = entry["date"].date() if pd.notna(entry["date"]) else None
            else:
                entry["date"] = None

        # Handle next_scheduled field
        if "next_scheduled" in entry:
            if entry["next_scheduled"]:
                entry["next_scheduled"] = pd.to_datetime(entry["next_scheduled"], errors="coerce")
                entry["next_scheduled"] = (
                    entry["next_scheduled"].date() if pd.notna(entry["next_scheduled"]) else None
                )
            else:
                entry["next_scheduled"] = None

        # Replace empty strings with None for any other keys
        for key, value in entry.items():
            if value == "" or value is None:
                entry[key] = None

    return [MaintenanceLog(**entry) for entry in data]

# Load and Store Data
EQUIPMENT_DATA = load_equipment(EQUIPMENT_FILE)
MAINTENANCE_DATA = load_maintenance(MAINTENANCE_FILE)

# Extraction Functions
def extract_equipment_entities():
    """
    Return a sorted list of tuples (equipment_id, equipment_type).
    This matches the requirement to extract equipment entities.
    """
    return sorted({(e.equipment_id, e.equipment_type) for e in EQUIPMENT_DATA})


def extract_locations():
    """Return a sorted list of equipment locations."""
    return sorted({e.location for e in EQUIPMENT_DATA})


def extract_maintenance_types():
    """Return a sorted list of maintenance types."""
    return sorted({m.maintenance_type for m in MAINTENANCE_DATA})
