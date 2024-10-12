from fastapi import APIRouter, HTTPException, status, Query
from app.models.items import ItemModel
from app.schemas.items import ItemCreateSchema, ItemResponseSchema, ItemUpdateSchema, ItemCountByEmailSchema
from app.database import db
from bson import ObjectId
from datetime import datetime
from typing import Optional, List, Union

router = APIRouter()

items_collection = db["Items"]

# Create a new item
@router.post("/", response_model=ItemResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreateSchema):
    new_item = ItemModel(**item.model_dump())  # Insert data into ItemModel
    try:
        result = await items_collection.insert_one(new_item.model_dump(by_alias=True))  # Insert item into MongoDB
        created_item = await items_collection.find_one({"_id": result.inserted_id})  # Retrieve the newly created item
            
        if created_item:
            created_item["id"] = str(created_item["_id"])  # Convert PyObjectId to string
            return ItemResponseSchema(**created_item)
    except Exception as e:
        print(f"Error inserting item: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item could not be created")


# Retrieve an item by ID 
@router.get("/{id}", response_model=ItemResponseSchema)
async def get_item_by_id(id: str):
    # Validate that the provided id is a valid MongoDB ObjectId
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid item ID format")

    item = await items_collection.find_one({"_id": ObjectId(id)}) # Query to find document

    if item:
        item["id"] = str(item["_id"])  # Convert ObjectId to string
        return ItemResponseSchema(**item)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")


# Update an item by ID
@router.put("/{id}", response_model=ItemResponseSchema)
async def update_item(id: str, item: ItemUpdateSchema):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid item ID format")
    
    update_data = item.model_dump(exclude_unset=True)  # Update only fields that are provided (excluding insert_date)
    
    result = await items_collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})

    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    updated_item = await items_collection.find_one({"_id": ObjectId(id)})
    
    if updated_item:
        updated_item["id"] = str(updated_item["_id"])
        return ItemResponseSchema(**updated_item)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")


# Delete an item by ID
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid item ID format")
    
    result = await items_collection.delete_one({"_id": ObjectId(id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    return {"message": "Item deleted successfully"}


# Filter and/or Aggregate item records
@router.get("/filter/", response_model=Union[List[ItemResponseSchema], List[ItemCountByEmailSchema]])
async def filter_and_aggregate_items(
    email: Optional[str] = Query(None, description="Exact email match"),
    expiry_date: Optional[datetime] = Query(None, description="Items expiring after this date"),
    insert_date: Optional[datetime] = Query(None, description="Items inserted after this date"),
    quantity: Optional[int] = Query(None, description="Quantity greater than or equal to this value"),
    aggregate: bool = Query(False,description="Set to perform aggregation")
):
    # Build the filter query dynamically based on the input filters
    filter_query = {}

    if email:
        filter_query["email"] = email

    if expiry_date:
        filter_query["expiry_date"] = {"$gt": expiry_date}

    if insert_date:
        filter_query["insert_date"] = {"$gt": insert_date}

    if quantity:
        filter_query["quantity"] = {"$gte": quantity}


    if aggregate:
        # MongoDB aggregation pipeline
        pipeline = [
            {"$match": filter_query},  # Apply filters
            {"$group": {"_id": "$email", "count": {"$sum": 1}}},  # Group by email and count items
            {"$project": {"_id": 0, "email": "$_id", "count": 1}}  # Format output
        ]
        aggregated_result = await items_collection.aggregate(pipeline).to_list(length=None)

        return [ItemCountByEmailSchema(**agg) for agg in aggregated_result]
    else:
        # Normal filtering
        items = await items_collection.find(filter_query).to_list(length=None)
        for item in items:
            item["id"] = str(item["_id"])
        return [ItemResponseSchema(**item) for item in items]