from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class ItemCreateSchema(BaseModel):
    name: str = Field(..., example="Rahul Sharma")
    email: EmailStr = Field(..., example="rahul@gmail.com")
    item_name: str = Field(..., example="Milk")
    quantity: int = Field(..., example=2)
    expiry_date: datetime = Field(..., example="2024-12-31")  

class ItemResponseSchema(ItemCreateSchema):
    id: str = Field(..., example="614d25f4fc13ae1c5d123456")
    insert_date: datetime = Field(..., example="2024-10-11T00:00:00Z")

    class Config:
        from_attributes = True

class ItemUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, example="Rahul Sharma")
    email: Optional[EmailStr] = Field(None, example="rahul@gmail.com")
    item_name: Optional[str] = Field(None, example="Milk")
    quantity: Optional[int] = Field(None, example=2)
    expiry_date: Optional[datetime] = Field(None, example="2024-12-31")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Ramesh Mehta",
                "email": "ramesh@example.com",
                "item_name": "Bread",
                "quantity": 5,
                "expiry_date": "2025-01-15"
            }
        }

class ItemCountByEmailSchema(BaseModel):
    email: EmailStr = Field(..., example="rahul@gmail.com")
    count: int = Field(..., example=2)