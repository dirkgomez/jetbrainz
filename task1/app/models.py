from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database import Base

# Association table for many-to-many relationship between ShopItem and ShopItemCategory
shop_item_category_association = Table(
    'shop_item_category_association',
    Base.metadata,
    Column('shop_item_id', Integer, ForeignKey('shop_items.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('shop_item_categories.id'), primary_key=True)
)

class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    surname = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    
    # Relationship with orders
    orders = relationship("Order", back_populates="customer")

class ShopItemCategory(Base):
    __tablename__ = "shop_item_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    
    # Many-to-many relationship with shop items
    shop_items = relationship("ShopItem", secondary=shop_item_category_association, back_populates="categories")

class ShopItem(Base):
    __tablename__ = "shop_items"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    
    # Many-to-many relationship with categories
    categories = relationship("ShopItemCategory", secondary=shop_item_category_association, back_populates="shop_items")
    
    # Relationship with order items
    order_items = relationship("OrderItem", back_populates="shop_item")

class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    shop_item_id = Column(Integer, ForeignKey("shop_items.id"))
    quantity = Column(Integer)
    order_id = Column(Integer, ForeignKey("orders.id"))
    
    # Relationships
    shop_item = relationship("ShopItem", back_populates="order_items")
    order = relationship("Order", back_populates="items")

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    
    # Relationships
    customer = relationship("Customer", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")
