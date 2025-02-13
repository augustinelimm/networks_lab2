from fastapi import FastAPI, Depends, HTTPException, Query, UploadFile, File, Header
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
from pydantic import BaseModel
from typing import Optional
import shutil 

class ItemCreate(BaseModel):
    id: Optional[int] = None
    name: str
    stock: int

class ItemUpdate(BaseModel):
    id: Optional[int]
    name: Optional[str]
    stock: Optional[int]

# Database connection set up
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the database model
class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    stock = Column(Integer, nullable=False)

# Database session dependency
# Each db request get its own session and is closed after use
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()


'''
GET REQUEST
'''
@app.get("/")
def read_root():
    return {
        "message": "Welcome! You can use this API to check clothing stock.",
        "Challenges": {"File upload in a POST request, using multipart/form-data",
                       "Authorisation through inspecting request header for DELETE request"
        },
        "Note": {
            "For testing, .http files are placed in checkoff folder. test_api.py shows tests for idempotency"
        }
    }

@app.get("/items")
def get_items(
    db: Session = Depends(get_db),
    sortBy: Optional[str] = Query(None, description="Attribute to sort by"),
    count: Optional[int] = Query(None, description="Limit number of items returned")
):
    query = db.query(Item)
    
    # Sorting logic
    if sortBy in ["id", "name", "stock"]:
        query = query.order_by(getattr(Item, sortBy))
    
    # Limit results if count is provided
    if count:
        query = query.limit(count)
    
    items = query.all()
    return [{"id": item.id, "name": item.name, "stock": item.stock} for item in items]

@app.get("/items/{item_id}")
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item.id, "name": item.name, "stock": item.stock}

'''
POST REQUEST
'''
@app.post("/items", status_code=201)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    errors = []

    # Validate required fields
    if item.name is None:
        errors.append("Name field is required.")
    if item.stock is None:
        errors.append("Stock field is required.")
    if item.stock is not None and item.stock < 0:
        errors.append("Stock must be a non-negative integer.")

    # Check for duplicate ID
    if item.id is not None:
        existing_item = db.query(Item).filter(Item.id == item.id).first()
        if existing_item:
            errors.append(f"Item with ID {item.id} already exists.")

    # Return validation errors
    if errors:
        return {"status": "error", "message": "Validation failed", "errors": errors}

    new_item = Item(**item.dict(exclude_unset=True))
    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return {
        "status": "success",
        "message": "Item created successfully",
        "data": {"id": new_item.id, "name": new_item.name, "stock": new_item.stock}
    }

'''
DELETE REQUEST
'''
@app.delete("/items/{item_id}", status_code=200)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()

    if not item:
        return {"message": f"Item with ID {item_id} not found. No deletion performed."}

    db.delete(item)
    db.commit()

    return {"message": f"Item with ID {item_id} has been successfully deleted."}

'''
PUT REQUEST (UPDATE ITEM)
'''
@app.put("/items/{item_id}")
def update_item(item_id: int, item_update: ItemUpdate, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    if item_update.id is not None and item_update.id != item.id:
        existing_id = db.query(Item).filter(Item.id == item_update.id).first()
        if existing_id:
            raise HTTPException(status_code=400, detail="ID already exists")
        item.id = item_update.id

    # Update name if provided
    if item_update.name:
        item.name = item_update.name

    # Update stock if provided
    if item_update.stock is not None:
        item.stock = item_update.stock

    db.commit()
    db.refresh(item)
    return {"id": item.id, "name": item.name, "stock": item.stock}

'''
FILE UPLOAD
'''
@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    save_directory = "uploads/"
    os.makedirs(save_directory, exist_ok=True)

    file_path = os.path.join(save_directory, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "status": "success",
        "message": f"File '{file.filename}' uploaded successfully.",
        "file_path": file_path
    }

'''
AUTHORIZATION TO DELETE
'''
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "password")

# Authorization Dependency
def check_admin_password(x_admin_password: str = Header(...)):
    if x_admin_password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid admin password")
    return True

# Protected Delete Request
@app.delete("/admin/items/{item_id}", status_code=200, dependencies=[Depends(check_admin_password)])
def admin_delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()

    if not item:
        return {"message": f"Item with ID {item_id} not found. No deletion performed."}

    db.delete(item)
    db.commit()

    return {"message": f"Item with ID {item_id} has been successfully deleted."}