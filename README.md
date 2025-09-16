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
├── README.md                 # Your documentation
├── requirements.txt          # Dependencies
├── main.py                  # Application entry point (FastAPI skeleton provided)
├── data/                    # Sample data files (provided)
│   ├── equipment_inventory.csv
│   └── maintenance_logs.json
├── src/                     # Your source code
│   ├── __init__.py
│   ├── data_processor.py    # Data processing logic
│   ├── api.py              # API endpoints
│   └── models.py           # Data models (optional)
└── tests/                   # Your tests
    ├── __init__.py
    └── test_*.py           # Test files
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