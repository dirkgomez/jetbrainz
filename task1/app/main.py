from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Table, Text, exc
from sqlalchemy.orm import sessionmaker, relationship, declarative_base, Session
from pydantic import BaseModel, EmailStr
from typing import List, Optional

DATABASE_URL = "sqlite:///./shop.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Association table for many-to-many relationship between ShopItem and ShopItemCategory
shopitem_category = Table(
    "shopitem_category",
    Base.metadata,
    Column("shopitem_id", Integer, ForeignKey("shop_items.id")),
    Column("category_id", Integer, ForeignKey("categories.id")),
)

class CustomerDB(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

class ShopItemCategoryDB(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)

class ShopItemDB(Base):
    __tablename__ = "shop_items"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    categories = relationship("ShopItemCategoryDB", secondary=shopitem_category, backref="shop_items")

class OrderItemDB(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    shop_item_id = Column(Integer, ForeignKey("shop_items.id"))
    quantity = Column(Integer, nullable=False)
    shop_item = relationship("ShopItemDB")
    order_id = Column(Integer, ForeignKey("orders.id"))  # <-- Add this line

class OrderDB(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    customer = relationship("CustomerDB")
    items = relationship("OrderItemDB", cascade="all, delete-orphan", backref="order")  # <-- Add backref

# Pydantic Schemas
class CustomerBase(BaseModel):
    name: str
    surname: str
    email: EmailStr

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int
    class Config:
        orm_mode = True

class ShopItemCategoryBase(BaseModel):
    title: str
    description: Optional[str] = None

class ShopItemCategoryCreate(ShopItemCategoryBase):
    pass

class ShopItemCategory(ShopItemCategoryBase):
    id: int
    class Config:
        orm_mode = True

class ShopItemBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    category_ids: List[int] = []

class ShopItemCreate(ShopItemBase):
    pass

class ShopItem(ShopItemBase):
    id: int
    categories: List[ShopItemCategory] = []
    class Config:
        orm_mode = True

class OrderItemBase(BaseModel):
    shop_item_id: int
    quantity: int

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int
    shop_item: ShopItem
    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    customer_id: int
    item_ids: List[int]

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    customer: Customer
    items: List[OrderItem]
    class Config:
        orm_mode = True

# FastAPI app
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- CRUD Endpoints ---

# Customer
@app.post("/customers/", response_model=Customer)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    db_customer = CustomerDB(**customer.dict())
    try:
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)
    except exc.IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")
    return db_customer

@app.get("/customers/", response_model=List[Customer])
def list_customers(db: Session = Depends(get_db)):
    return db.query(CustomerDB).all()

@app.get("/customers/{customer_id}", response_model=Customer)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(CustomerDB).get(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@app.put("/customers/{customer_id}", response_model=Customer)
def update_customer(customer_id: int, customer: CustomerCreate, db: Session = Depends(get_db)):
    db_customer = db.query(CustomerDB).get(customer_id)
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    for k, v in customer.dict().items():
        setattr(db_customer, k, v)
    db.commit()
    db.refresh(db_customer)
    return db_customer

@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = db.query(CustomerDB).get(customer_id)
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    db.delete(db_customer)
    db.commit()
    return {"ok": True}

# ShopItemCategory
@app.post("/categories/", response_model=ShopItemCategory)
def create_category(category: ShopItemCategoryCreate, db: Session = Depends(get_db)):
    db_category = ShopItemCategoryDB(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@app.get("/categories/", response_model=List[ShopItemCategory])
def list_categories(db: Session = Depends(get_db)):
    return db.query(ShopItemCategoryDB).all()

@app.get("/categories/{category_id}", response_model=ShopItemCategory)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(ShopItemCategoryDB).get(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@app.put("/categories/{category_id}", response_model=ShopItemCategory)
def update_category(category_id: int, category: ShopItemCategoryCreate, db: Session = Depends(get_db)):
    db_category = db.query(ShopItemCategoryDB).get(category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    for k, v in category.dict().items():
        setattr(db_category, k, v)
    db.commit()
    db.refresh(db_category)
    return db_category

@app.delete("/categories/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(ShopItemCategoryDB).get(category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(db_category)
    db.commit()
    return {"ok": True}

# ShopItem
@app.post("/shop_items/", response_model=ShopItem)
def create_shop_item(item: ShopItemCreate, db: Session = Depends(get_db)):
    categories = db.query(ShopItemCategoryDB).filter(ShopItemCategoryDB.id.in_(item.category_ids)).all()
    db_item = ShopItemDB(
        title=item.title,
        description=item.description,
        price=item.price,
        categories=categories
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/shop_items/", response_model=List[ShopItem])
def list_shop_items(db: Session = Depends(get_db)):
    return db.query(ShopItemDB).all()

@app.get("/shop_items/{item_id}", response_model=ShopItem)
def get_shop_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(ShopItemDB).get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="ShopItem not found")
    return item

@app.put("/shop_items/{item_id}", response_model=ShopItem)
def update_shop_item(item_id: int, item: ShopItemCreate, db: Session = Depends(get_db)):
    db_item = db.query(ShopItemDB).get(item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="ShopItem not found")
    categories = db.query(ShopItemCategoryDB).filter(ShopItemCategoryDB.id.in_(item.category_ids)).all()
    db_item.title = item.title
    db_item.description = item.description
    db_item.price = item.price
    db_item.categories = categories
    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/shop_items/{item_id}")
def delete_shop_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(ShopItemDB).get(item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="ShopItem not found")
    db.delete(db_item)
    db.commit()
    return {"ok": True}

# OrderItem
@app.post("/order_items/", response_model=OrderItem)
def create_order_item(order_item: OrderItemCreate, db: Session = Depends(get_db)):
    db_order_item = OrderItemDB(**order_item.dict())
    db.add(db_order_item)
    db.commit()
    db.refresh(db_order_item)
    return db_order_item

@app.get("/order_items/", response_model=List[OrderItem])
def list_order_items(db: Session = Depends(get_db)):
    return db.query(OrderItemDB).all()

@app.get("/order_items/{order_item_id}", response_model=OrderItem)
def get_order_item(order_item_id: int, db: Session = Depends(get_db)):
    order_item = db.query(OrderItemDB).get(order_item_id)
    if not order_item:
        raise HTTPException(status_code=404, detail="OrderItem not found")
    return order_item

@app.put("/order_items/{order_item_id}", response_model=OrderItem)
def update_order_item(order_item_id: int, order_item: OrderItemCreate, db: Session = Depends(get_db)):
    db_order_item = db.query(OrderItemDB).get(order_item_id)
    if not db_order_item:
        raise HTTPException(status_code=404, detail="OrderItem not found")
    db_order_item.shop_item_id = order_item.shop_item_id
    db_order_item.quantity = order_item.quantity
    db.commit()
    db.refresh(db_order_item)
    return db_order_item

@app.delete("/order_items/{order_item_id}")
def delete_order_item(order_item_id: int, db: Session = Depends(get_db)):
    db_order_item = db.query(OrderItemDB).get(order_item_id)
    if not db_order_item:
        raise HTTPException(status_code=404, detail="OrderItem not found")
    db.delete(db_order_item)
    db.commit()
    return {"ok": True}

# Order
@app.post("/orders/", response_model=Order)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    db_order = OrderDB(customer_id=order.customer_id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    # Add order items
    items = db.query(OrderItemDB).filter(OrderItemDB.id.in_(order.item_ids)).all()
    for item in items:
        item.order_id = db_order.id
    db.commit()
    db.refresh(db_order)
    # Compose item_ids for schema compatibility
    db_order.items = db.query(OrderItemDB).filter(OrderItemDB.order_id == db_order.id).all()
    for item in db_order.items:
        item.shop_item = db.query(ShopItemDB).get(item.shop_item_id)
    item_ids = [item.id for item in db_order.items]
    return {
        "id": db_order.id,
        "customer_id": db_order.customer_id,
        "item_ids": item_ids,
        "customer": db_order.customer,
        "items": db_order.items
    }

@app.get("/orders/", response_model=List[Order])
def list_orders(db: Session = Depends(get_db)):
    orders = db.query(OrderDB).all()
    result = []
    for order in orders:
        order.items = db.query(OrderItemDB).filter(OrderItemDB.order_id == order.id).all()
        for item in order.items:
            item.shop_item = db.query(ShopItemDB).get(item.shop_item_id)
        item_ids = [item.id for item in order.items]
        result.append({
            "id": order.id,
            "customer_id": order.customer_id,
            "item_ids": item_ids,
            "customer": order.customer,
            "items": order.items
        })
    return result

@app.put("/orders/{oid}", response_model=Order)
def update_order_by_oid(oid: int, order: OrderCreate, db: Session = Depends(get_db)):
    db_order = db.query(OrderDB).get(oid)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    db_order.customer_id = order.customer_id
    # Unassign all current order items
    db.query(OrderItemDB).filter(OrderItemDB.order_id == db_order.id).update({"order_id": None})
    db.commit()
    # Assign new order items
    items = db.query(OrderItemDB).filter(OrderItemDB.id.in_(order.item_ids)).all()
    for item in items:
        item.order_id = db_order.id
    db.commit()
    db.refresh(db_order)
    db_order.items = db.query(OrderItemDB).filter(OrderItemDB.order_id == db_order.id).all()
    for item in db_order.items:
        item.shop_item = db.query(ShopItemDB).get(item.shop_item_id)
    item_ids = [item.id for item in db_order.items]
    return {
        "id": db_order.id,
        "customer_id": db_order.customer_id,
        "item_ids": item_ids,
        "customer": db_order.customer,
        "items": db_order.items
    }

@app.delete("/orders/{oid}")
def delete_order_by_oid(oid: int, db: Session = Depends(get_db)):
    db_order = db.query(OrderDB).get(oid)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    db.query(OrderItemDB).filter(OrderItemDB.order_id == db_order.id).update({"order_id": None})
    db.commit()
    db.delete(db_order)
    db.commit()
    return {"ok": True}

# --- DB Initialization with test data ---
@app.on_event("startup")
def startup_populate():
    # --- Fix: ensure DB schema is up-to-date by dropping and recreating tables if needed ---
    import os
    if os.path.exists("shop.db"):
        os.remove("shop.db")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    if not db.query(CustomerDB).first():
        c1 = CustomerDB(name="Alice", surname="Smith", email="alice@example.com")
        c2 = CustomerDB(name="Bob", surname="Brown", email="bob@example.com")
        db.add_all([c1, c2])
        db.commit()
    if not db.query(ShopItemCategoryDB).first():
        cat1 = ShopItemCategoryDB(title="Books", description="All kinds of books")
        cat2 = ShopItemCategoryDB(title="Electronics", description="Gadgets and devices")
        db.add_all([cat1, cat2])
        db.commit()
    if not db.query(ShopItemDB).first():
        cat1 = db.query(ShopItemCategoryDB).filter_by(title="Books").first()
        cat2 = db.query(ShopItemCategoryDB).filter_by(title="Electronics").first()
        item1 = ShopItemDB(title="Python Book", description="Learn Python", price=29.99, categories=[cat1])
        item2 = ShopItemDB(title="Smartphone", description="Latest model", price=499.99, categories=[cat2])
        db.add_all([item1, item2])
        db.commit()
    if not db.query(OrderItemDB).first():
        item1 = db.query(ShopItemDB).filter_by(title="Python Book").first()
        item2 = db.query(ShopItemDB).filter_by(title="Smartphone").first()
        oi1 = OrderItemDB(shop_item_id=item1.id, quantity=2)
        oi2 = OrderItemDB(shop_item_id=item2.id, quantity=1)
        db.add_all([oi1, oi2])
        db.commit()
    if not db.query(OrderDB).first():
        c1 = db.query(CustomerDB).filter_by(name="Alice").first()
        oi1 = db.query(OrderItemDB).filter_by(quantity=2).first()
        oi2 = db.query(OrderItemDB).filter_by(quantity=1).first()
        order = OrderDB(customer_id=c1.id, items=[oi1, oi2])
        db.add(order)
        db.commit()
    db.close()

@app.get("/orders/{oid}", response_model=Order)
def get_order_by_oid(oid: int, db: Session = Depends(get_db)):
    order = db.query(OrderDB).get(oid)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.items = db.query(OrderItemDB).filter(OrderItemDB.order_id == order.id).all()
    for item in order.items:
        item.shop_item = db.query(ShopItemDB).get(item.shop_item_id)
    item_ids = [item.id for item in order.items]
    return {
        "id": order.id,
        "customer_id": order.customer_id,
        "item_ids": item_ids,
        "customer": order.customer,
        "items": order.items
    }

# --- Order by_oid(oid: int, order: OrderCreate, db: Session = Depends(get_db)):
# Unassign all current order items
    db.query(OrderItemDB).filter(OrderItemDB.order_id == db_order.id).update({"order_id": None})
    db.commit()
    # Assign new order items
    items = db.query(OrderItemDB).filter(OrderItemDB.id.in_(order.item_ids)).all()
    for item in items:
        item.order_id = db_order.id
    db.commit()
    db.refresh(db_order)
    db_order.items = db.query(OrderItemDB).filter(OrderItemDB.order_id == db_order.id).all()
    for item in db_order.items:
        item.shop_item = db.query(ShopItemDB).get(item.shop_item_id)
    item_ids = [item.id for item in db_order.items]
    return {
        "id": db_order.id,
        "customer_id": db_order.customer_id,
        "item_ids": item_ids,
        "customer": db_order.customer,
        "items": db_order.items
    }

# --- Order by_oid(oid: int, order: OrderCreate, db: Session = Depends(get_db)):
# Unassign all current order items
    db.query(OrderItemDB).filter(OrderItemDB.order_id == db_order.id).update({"order_id": None})
    db.commit()
    # Assign new order items
    items = db.query(OrderItemDB).filter(OrderItemDB.id.in_(order.item_ids)).all()
    for item in items:
        item.order_id = db_order.id
    db.commit()
    db.refresh(db_order)
    db_order.items = db.query(OrderItemDB).filter(OrderItemDB.order_id == db_order.id).all()
    for item in db_order.items:
        item.shop_item = db.query(ShopItemDB).get(item.shop_item_id)
    item_ids = [item.id for item in db_order.items]
    return {
        "id": db_order.id,
        "customer_id": db_order.customer_id,
        "item_ids": item_ids,
        "customer": db_order.customer,
        "items": db_order.items
    }