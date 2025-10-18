# Streamoid Product Catalog Backend

A FastAPI backend service for uploading, validating, storing, listing, and searching product data from CSV files.  
Designed for online sellers to manage and validate their product catalog before listing on marketplaces.

---

## Features

- **CSV Upload & Validation:** Upload product data, validate required fields, price, quantity, and duplicate SKUs.
- **Database Storage:** Store valid products in SQLite (default).
- **REST APIs:** List all products (with pagination) and search/filter by brand, color, and price range.
- **Dockerized:** Easy deployment using Docker.
- **Unit Tests:** Test CSV parsing, validation, and search filters.

---

## Getting Started

### Prerequisites

- Python 3.8+ (if running without Docker)
- [Docker Desktop](https://www.docker.com/products/docker-desktop) (if using Docker)

---

### 1. Clone the Repository
git clone <your-repo-url> cd <your-repo-folder>

---

### 2. Install Dependencies (Without Docker)
pip install -r requirements.txt

---

### 3. Run the Application (Without Docker)
uvicorn main:app --reload --host 0.0.0.0 --port 8000
The API will be available at `http://localhost:8000`.
- The API will be available at [http://localhost:8000](http://localhost:8000)
- Interactive docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

### 4. Run with Docker

#### Build the Docker Image
docker build -t streamoid-backend .

#### Run the Docker Container
docker run -p 8000:8000 streamoid-backend

The API will be available at `http://localhost:8000`.

---

### 5. Run Tests

- All tests are located in the `tests/` directory.
- command : `pytest` from root repository

---

## API Documentation

### 1. Upload CSV

**Endpoint:**  
`POST /upload`

**Description:**  
Upload a CSV file containing product data. Validates each row and stores valid products.

**Request:**  
- Form-data: `file` (CSV file)

---

### 2. List Products

**Endpoint:**  
`GET /products`

**Description:**  
Returns all stored products with pagination.

**Query Parameters:**
- `page` (default: 1)
- `limit` (default: 10, max: 100)


---

### 3. Search Products

**Endpoint:**  
`GET /products/search`

**Description:**  
Filter products by brand, color, and price range.

**Query Parameters:**
- `brand` (optional)
- `color` (optional)
- `minPrice` (optional)
- `maxPrice` (optional)

### 4. Root Endpoint

**Endpoint:**  
`GET /`

## Project Structure
. ├── main.py ├── models.py ├── database.py ├── schemas.py ├── requirements.txt ├── Dockerfile ├── .dockerignore ├── tests/ │   └── test_main.py ├── products.csv └── README.md


## Notes

- The API docs are available at `/docs` (Swagger UI).