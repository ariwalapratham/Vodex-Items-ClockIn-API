from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId
from app.models.custom_types import PyObjectId
from datetime import datetime, timezone

class ClockInModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    email: EmailStr
    location: str
    insert_date: datetime = Field(default_factory= lambda: datetime.now(timezone.utc))

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda dt: dt.isoformat()
        }