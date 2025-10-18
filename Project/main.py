from fastapi import FastAPI, File, UploadFile, HTTPException, Query, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
import csv
import io

from models import Base, Product
from database import engine, get_db, SessionLocal
from schemas import ProductOut, UploadResponse

app = FastAPI()

Base.metadata.create_all(bind=engine)

REQUIRED_FIELDS = ["sku", "name", "brand", "mrp", "price"]

def validate_row(row):
    errors = []
    for field in REQUIRED_FIELDS:
        if not row.get(field):
            errors.append(f"Missing {field}")
    try:
        mrp = int(row.get("mrp", 0))
        price = int(row.get("price", 0))
        quantity = int(row.get("quantity", 0))
    except ValueError:
        errors.append("mrp, price, quantity must be integers")
        return False, errors
    if price > mrp:
        errors.append("price must be ≤ mrp")
    if quantity < 0:
        errors.append("quantity must be ≥ 0")
    return len(errors) == 0, errors

@app.post("/upload", response_model=UploadResponse)
def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = file.file.read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(content))
    stored = 0
    failed = []
    for idx, row in enumerate(reader, start=2):
        valid, errors = validate_row(row)
        if not valid:
            failed.append({"row": idx, "errors": errors})
            continue
        # Check for duplicate SKU
        if db.query(Product).filter_by(sku=row["sku"]).first():
            failed.append({"row": idx, "errors": ["Duplicate SKU"]})
            continue
        product = Product(
            sku=row["sku"],
            name=row["name"],
            brand=row["brand"],
            color=row.get("color"),
            size=row.get("size"),
            mrp=int(row["mrp"]),
            price=int(row["price"]),
            quantity=int(row.get("quantity", 0)),
        )
        db.add(product)
        stored += 1
    db.commit()
    return UploadResponse(stored=stored, failed=failed)

@app.get("/products", response_model=List[ProductOut])
def list_products(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    offset = (page - 1) * limit
    products = db.query(Product).offset(offset).limit(limit).all()
    return products

@app.get("/products/search", response_model=List[ProductOut])
def search_products(
    brand: Optional[str] = None,
    color: Optional[str] = None,
    minPrice: Optional[int] = None,
    maxPrice: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Product)
    if brand:
        query = query.filter(func.lower(Product.brand) == brand.lower())
    if color:
        query = query.filter(func.lower(Product.color) == color.lower())
    if minPrice is not None:
        query = query.filter(Product.price >= minPrice)
    if maxPrice is not None:
        query = query.filter(Product.price <= maxPrice)
    return query.all()

@app.get("/")
def read_root():
    return {"message": "Streamoid Product API is running. See /docs for API documentation."}