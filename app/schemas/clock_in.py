from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class ClockInCreateSchema(BaseModel):
    email: EmailStr = Field(..., example="rahul@gmail.com")
    location: str = Field(..., example="Mumbai")

class ClockInResponseSchema(ClockInCreateSchema):
    id: str = Field(..., example="614d25f4fc13ae1c5d123456")
    insert_date: datetime = Field(..., example="2024-10-11T00:00:00Z")

    class Config:
        from_attributes = True

class ClockInUpdateSchema(BaseModel):
    email: Optional[EmailStr]
    location: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "email": "ramesh@example.com",
                "location": "Pune"
            }
        }