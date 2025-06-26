from fastapi import FastAPI
from app import models
from app.database import engine
from app.routers import customers, categories, items, orders

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Online Shop API",
    description="A minimalistic backend web application for an online shop",
    version="1.0.0"
)

# Include routers
app.include_router(customers.router, tags=["customers"])
app.include_router(categories.router, tags=["categories"])
app.include_router(items.router, tags=["items"])
app.include_router(orders.router, tags=["orders"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Online Shop API"}

# Initialize sample data
@app.on_event("startup")
def startup_event():
    from app.database import SessionLocal
    from app import crud, schemas
    
    db = SessionLocal()
    try:
        # Check if data already exists
        existing_customers = crud.get_customers(db, limit=1)
        if existing_customers:
            return  # Data already initialized
        
        # Create sample customers
        customers_data = [
            {"name": "John", "surname": "Doe", "email": "john.doe@example.com"},
            {"name": "Jane", "surname": "Smith", "email": "jane.smith@example.com"},
            {"name": "Bob", "surname": "Johnson", "email": "bob.johnson@example.com"}
        ]
        
        for customer_data in customers_data:
            customer = schemas.CustomerCreate(**customer_data)
            crud.create_customer(db, customer)
        
        # Create sample categories
        categories_data = [
            {"title": "Electronics", "description": "Electronic devices and gadgets"},
            {"title": "Clothing", "description": "Clothing and fashion items"},
            {"title": "Books", "description": "Books and educational materials"},
            {"title": "Home & Garden", "description": "Home and garden supplies"}
        ]
        
        for category_data in categories_data:
            category = schemas.ShopItemCategoryCreate(**category_data)
            crud.create_category(db, category)
        
        # Create sample shop items
        items_data = [
            {"title": "Smartphone", "description": "Latest smartphone with advanced features", "price": 599.99, "category_ids": [1]},
            {"title": "Laptop", "description": "High-performance laptop for work and gaming", "price": 1299.99, "category_ids": [1]},
            {"title": "T-Shirt", "description": "Comfortable cotton t-shirt", "price": 19.99, "category_ids": [2]},
            {"title": "Jeans", "description": "Classic blue jeans", "price": 49.99, "category_ids": [2]},
            {"title": "Python Programming Book", "description": "Learn Python programming from scratch", "price": 39.99, "category_ids": [3]},
            {"title": "Garden Tools Set", "description": "Complete set of garden tools", "price": 79.99, "category_ids": [4]}
        ]
        
        for item_data in items_data:
            item = schemas.ShopItemCreate(**item_data)
            crud.create_shop_item(db, item)
        
        # Create sample orders
        orders_data = [
            {
                "customer_id": 1,
                "items": [
                    {"shop_item_id": 1, "quantity": 1},
                    {"shop_item_id": 3, "quantity": 2}
                ]
            },
            {
                "customer_id": 2,
                "items": [
                    {"shop_item_id": 2, "quantity": 1},
                    {"shop_item_id": 5, "quantity": 1}
                ]
            }
        ]
        
        for order_data in orders_data:
            order = schemas.OrderCreate(**order_data)
            crud.create_order(db, order)
        
    finally:
        db.close()
