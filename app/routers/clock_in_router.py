from fastapi import APIRouter, HTTPException, status, Query
from app.models.clock_in import ClockInModel
from app.schemas.clock_in import ClockInCreateSchema, ClockInResponseSchema, ClockInUpdateSchema
from app.database import db
from bson import ObjectId
from datetime import datetime
from typing import Optional, List

router = APIRouter()

clock_in_collection = db["User Clock-In Records"]

# Create a new clock-in entry
@router.post("/", response_model=ClockInResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_clock_in(clock_in: ClockInCreateSchema):
    new_clock_in = ClockInModel(**clock_in.model_dump())
    try:
        result = await clock_in_collection.insert_one(new_clock_in.model_dump(by_alias=True))
        created_clock_in = await clock_in_collection.find_one({"_id": result.inserted_id})
        
        if created_clock_in:
            created_clock_in["id"] = str(created_clock_in["_id"])
            return ClockInResponseSchema(**created_clock_in)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Clock-in could not be created")


# Retrieve a clock-in record by ID
@router.get("/{id}", response_model=ClockInResponseSchema)
async def get_clock_in_by_id(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid clock-in ID format")

    clock_in_record = await clock_in_collection.find_one({"_id": ObjectId(id)})

    if clock_in_record:
        clock_in_record["id"] = str(clock_in_record["_id"])
        return ClockInResponseSchema(**clock_in_record)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Clock-in record not found")


# Filter clock-in records
@router.get("/filter/", response_model=List[ClockInResponseSchema])
async def filter_clock_in_records(
    email: Optional[str] = Query(None, description="Exact email match"),
    location: Optional[str] = Query(None, description="Exact location match"),
    insert_date: Optional[datetime] = Query(None, description="Clock-ins after this date (yyyy-mm-dd)"),
):
    # Build query based on optional parameters
    filter_query = {}
    
    if email:
        filter_query["email"] = email
    if location:
        filter_query["location"] = location
    if insert_date:
        filter_query["insert_date"] = {"$gt": insert_date}
    
    try:
        # Query MongoDB
        clock_in_records = await clock_in_collection.find(filter_query).to_list(length=None)
        
        if not clock_in_records:
            raise HTTPException(status_code=404, detail="No clock-in records found")
        
        # Convert PyObjectId to string and prepare the response
        for record in clock_in_records:
            record["id"] = str(record["_id"])
        
        return [ClockInResponseSchema(**record) for record in clock_in_records]
    
    except HTTPException as http_err:
        raise http_err  # Reraise specific HTTP exceptions
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while fetching the clock-in records")


# Delete a clock-in record by ID
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_clock_in(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid clock-in ID format")

    result = await clock_in_collection.delete_one({"_id": ObjectId(id)}) # Delete operation

    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Clock-in record not found")


# Update a clock-in record by ID
@router.put("/{id}", response_model=ClockInResponseSchema)
async def update_clock_in(id: str, clock_in: ClockInUpdateSchema):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid clock-in ID format")

    update_data = clock_in.model_dump(exclude_unset=True)  # Only update fields that are provided
    result = await clock_in_collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})

    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Clock-in record not found")

    updated_record = await clock_in_collection.find_one({"_id": ObjectId(id)})
    
    if updated_record:
        updated_record["id"] = str(updated_record["_id"])
        return ClockInResponseSchema(**updated_record)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Clock-in record not found")