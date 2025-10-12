"""
Basic tests for data processing and API endpoints.
"""

from fastapi.testclient import TestClient
from main import app
from src.data_processor import (
    EQUIPMENT_DATA,
    MAINTENANCE_DATA,
    extract_equipment_entities,
    extract_locations,
    extract_maintenance_types,
)

client = TestClient(app)

# Data Processor Tests

class TestDataProcessor:
    def test_load_csv_data(self):
        """Ensure equipment data is loaded correctly."""
        assert len(EQUIPMENT_DATA) > 0
        assert hasattr(EQUIPMENT_DATA[0], "equipment_id")

    def test_load_json_data(self):''
        """Ensure maintenance data is loaded correctly."""
        assert len(MAINTENANCE_DATA) > 0
        assert hasattr(MAINTENANCE_DATA[0], "maintenance_type")

    def test_extract_entities(self):
        """Check that entity extraction helpers return expected types."""
        equipment = extract_equipment_entities()
        locations = extract_locations()
        maintenance_types = extract_maintenance_types()

        assert isinstance(equipment, list)
        assert all(isinstance(item, tuple) for item in equipment)

        assert isinstance(locations, list)
        assert any("station" in loc.lower() for loc in locations)

        assert isinstance(maintenance_types, list)
        assert any(mt for mt in maintenance_types)


# API Tests

class TestAPI:
    def test_get_equipment_endpoint(self):
        """Test equipment listing endpoint."""
        response = client.get("/api/equipment")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert "equipment_id" in data[0]

    def test_search_endpoint(self):
        """Test search functionality."""
        response = client.get("/api/search", params={"query": "EQ001"})
        assert response.status_code == 200
        data = response.json()
        assert "equipment_matches" in data or "maintenance_matches" in data

    def test_info_endpoint(self):
        """Test info endpoint returns metadata."""
        response = client.get("/api/info")
        assert response.status_code == 200
        data = response.json()
        assert "unique_locations" in data
        assert "maintenance_types" in data

    def test_export_endpoint_json(self):
        """Test the export endpoint returns valid JSON."""
        response = client.get("/api/export", params={"format": "json"})
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert any("equipment_id" in item for item in data)

    def test_export_endpoint_csv(self):
        """Test the export endpoint returns CSV format."""
        response = client.get("/api/export", params={"format": "csv"})
        assert response.status_code == 200
        assert "text/csv" in response.headers["content-type"]
        assert "equipment_id" in response.text.splitlines()[0]