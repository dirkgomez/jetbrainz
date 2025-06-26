from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, models, schemas
from app.database import get_db

router = APIRouter()

@router.post("/items/", response_model=schemas.ShopItem)
def create_shop_item(item: schemas.ShopItemCreate, db: Session = Depends(get_db)):
    return crud.create_shop_item(db=db, item=item)

@router.get("/items/", response_model=List[schemas.ShopItem])
def read_shop_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_shop_items(db, skip=skip, limit=limit)
    return items

@router.get("/items/{item_id}", response_model=schemas.ShopItem)
def read_shop_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_shop_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Shop item not found")
    return db_item

@router.put("/items/{item_id}", response_model=schemas.ShopItem)
def update_shop_item(item_id: int, item: schemas.ShopItemUpdate, db: Session = Depends(get_db)):
    db_item = crud.update_shop_item(db, item_id=item_id, item=item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Shop item not found")
    return db_item

@router.delete("/items/{item_id}", response_model=schemas.ShopItem)
def delete_shop_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.delete_shop_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Shop item not found")
    return db_item
