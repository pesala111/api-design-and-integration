# API Design & Integration - Equipment Maintenance API

A lightweight FastAPI application that processes equipment and maintenance data, extracts key entities, and exposes them via RESTful API endpoints.

## Features
- Loads and validates equipment inventory (CSV) and maintenance logs (JSON).  
- Extracts and relates key entities with Pydantic schemas.  
- Provides endpoints to search, list, and export data.  
- Supports JSON and CSV export.  
- Includes unit tests for data processing and API endpoints.  
- Automatically generates interactive API documentation at `/docs`.  
- Containerized with Docker and includes CI workflow for testing.

---

### Project Structure

```
api-design-and-integration/
├── .github/
│   └── workflows/
│       └── ci.yml                  # CI workflow for automated testing
├── data/                           # Sample data files
│   ├── equipment_inventory.csv
│   └── maintenance_logs.json
├── src/                            
│   ├── __init__.py
│   ├── api.py                      # API endpoints (list, search, export)
│   ├── data_processor.py           # Data processing logic
│   └── models.py                   # Data models (Pydantic schemas)
├── tests/                          
│   ├── __init__.py
│   └── test_app.py                 # Unit tests for API and data processing
├── .gitignore                      
├── Dockerfile                      # Containerization setup
├── README.md                       
├── requirements.txt                
├── main.py                         # FastAPI app entry point
```

---

# Setup Instructions

## 🚀 Quick Start

### 1. Environment Setup
#### Create virtual environment (recommended)
```bash
python3 -m venv venv
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

### 3. Run with Docker

```bash
docker build -t api-demo .
docker run -p 8000:8000 api-demo
```

### 4. Running Tests
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

## Possible Use Cases
- Backend service for managing equipment inventories and maintenance logs.  
- API integration layer for IoT or monitoring systems that generate maintenance events.  
- Demo project to showcase clean API design, data validation, and integration patterns.  
- Educational example for building scalable FastAPI services with testing, CI/CD, and Docker.  
