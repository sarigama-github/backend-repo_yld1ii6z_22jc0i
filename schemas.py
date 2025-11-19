"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional

# Existing example schemas (kept for reference)
class User(BaseModel):
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Citywide Investors schemas
class FileDoc(BaseModel):
    filename: str
    content_type: Optional[str] = None
    size: Optional[int] = None
    content: Optional[bytes] = None  # raw bytes stored directly

class Submission(BaseModel):
    property_address: str
    guide_price: Optional[str] = None
    rental_income_occupancy: Optional[str] = None
    issues: Optional[str] = None
    contact_details: str
    file_id: Optional[str] = None
    source_ip: Optional[str] = None
