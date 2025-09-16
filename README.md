# Utility Knowledge API

A lightweight FastAPI application that processes equipment and maintenance data, extracts key entities, and exposes them via RESTful API endpoints.

## 📋 Features
- Loads and validates **equipment inventory** (CSV) and **maintenance logs** (JSON).  
- Extracts and relates key entities:  
- Provides endpoints to search, list, and export data.  
- Supports **JSON** and **CSV** export.  
- Includes unit tests for data processing and API endpoints.  
- Automatically generates interactive API documentation at `/docs`.

---

### Project Structure

```
utility-knowledge-api/
├── .github/
│   └── workflows/
│       └── ci.yml                  # CI workflow for automated testing
├── data/                           # Sample data files
│   ├── equipment_inventory.csv
│   └── maintenance_logs.json
├── src/                            # Source code
│   ├── __init__.py
│   ├── api.py                      # API endpoints (list, search, export)
│   ├── data_processor.py           # Data processing logic
│   └── models.py                   # Data models (Pydantic schemas)
├── tests/                          # Unit tests
│   ├── __init__.py
│   └── test_app.py                 # Unit tests for API and data processing
├── .gitignore                      # Git ignore rules
├── Dockerfile                      # Containerization setup
├── README.md                       # Project documentation
├── requirements.txt                # Dependencies
├── main.py                         # FastAPI app entry point
```

---

# Setup Instructions

## 🚀 Quick Start

### 1. Environment Setup
#### Create virtual environment (recommended)
```bash
python -m venv venv
```

### Activate virtual environment
### On Windows:
```bash
venv\Scripts\activate
```
### On macOS/Linux:
```bash
source venv/bin/activate
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
---
```bash
python main.py
```
### or
```bash
uvicorn main:app --reload
```
For interactive API documentation visit:

http://localhost:8000/docs
 (Swagger UI)

http://localhost:8000/redoc
 (ReDoc)

### 3. Running Tests
---

```bash
pytest -v
```

---

🔗 API Endpoints
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/equipment` | List all equipment inventory entries. |
| `GET` | `/api/maintenance` | List all maintenance logs. |
| `GET` | `/api/info` | Get unique equipment types, locations, and maintenance types. |
| `GET` | `/api/search` | Search across entities. |
| `GET` | `/api/export` | Export combined data as JSON or CSV. |

Example:
```bash
curl "http://localhost:8000/api/export?format=csv" -o export.csv
```

## 📌 Assumptions & Design Decisions
- Missing or malformed dates are handled.

- Maintenance and equipment records are linked via equipment_id, which is common key.

- All Bonus features implemented

- Single test file used for simplicity.

- Added **Dockerfile** for containerization and a **CI workflow** for automated testing (verified locally), even though these were not explicitly requested.  