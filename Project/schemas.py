from pydantic import BaseModel
from typing import List, Dict, Any

class ProductOut(BaseModel):
    sku: str
    name: str
    brand: str
    color: str = None
    size: str = None
    mrp: int
    price: int
    quantity: int

    model_config = {
        "from_attributes": True
    }

class UploadResponse(BaseModel):
    stored: int
    failed: List[Dict[str, Any]]