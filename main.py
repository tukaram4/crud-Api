from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Python CRUD API")

# --- 1. Data Model (Schema) ---
class Item(BaseModel):
    id: int
    name: str
    price: float
    description: Optional[str] = None

# --- 2. In-Memory Database Simulation ---
db_store: List[Item] = []

# --- 3. CRUD Endpoints ---

# CREATE: Add a new item
@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    # Check if ID already exists
    for existing_item in db_store:
        if existing_item.id == item.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Item with this ID already exists."
            )
    db_store.append(item)
    return item

# READ (All): Get all items
@app.get("/items", response_model=List[Item])
async def read_all_items():
    return db_store

# READ (One): Get a specific item by ID
@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    for item in db_store:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

# UPDATE: Modify an existing item completely
@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, updated_item: Item):
    for index, item in enumerate(db_store):
        if item.id == item_id:
            db_store[index] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")

# DELETE: Erase an item by ID
@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    for index, item in enumerate(db_store):
        if item.id == item_id:
            db_store.pop(index)
            return  # HTTP 204 requires an empty response body
    raise HTTPException(status_code=404, detail="Item not found")
