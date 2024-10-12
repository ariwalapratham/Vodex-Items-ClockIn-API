from pydantic import BaseModel, Field, EmailStr, field_serializer
from bson import ObjectId
from datetime import datetime, timezone
from app.models.custom_types import PyObjectId

class ItemModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    email: EmailStr
    item_name: str
    quantity: int
    expiry_date: datetime
    insert_date: datetime = Field(default_factory= lambda: datetime.now(timezone.utc))

    @field_serializer("expiry_date")
    def serialize_expiry_date(self, value: datetime) -> str:
        return value.strftime("%Y-%m-%d")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: lambda dt: dt.isoformat()}
