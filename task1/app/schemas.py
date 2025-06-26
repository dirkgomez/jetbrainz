from pydantic import BaseModel, EmailStr
from typing import List, Optional

# Customer schemas
class CustomerBase(BaseModel):
    name: str
    surname: str
    email: str

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int
    
    class Config:
        from_attributes = True

# ShopItemCategory schemas
class ShopItemCategoryBase(BaseModel):
    title: str
    description: str

class ShopItemCategoryCreate(ShopItemCategoryBase):
    pass

class ShopItemCategoryUpdate(ShopItemCategoryBase):
    pass

class ShopItemCategory(ShopItemCategoryBase):
    id: int
    
    class Config:
        from_attributes = True

# ShopItem schemas
class ShopItemBase(BaseModel):
    title: str
    description: str
    price: float

class ShopItemCreate(ShopItemBase):
    category_ids: List[int] = []

class ShopItemUpdate(ShopItemBase):
    category_ids: List[int] = []

class ShopItem(ShopItemBase):
    id: int
    categories: List[ShopItemCategory] = []
    
    class Config:
        from_attributes = True

# OrderItem schemas
class OrderItemBase(BaseModel):
    shop_item_id: int
    quantity: int

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemUpdate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int
    shop_item: ShopItem
    
    class Config:
        from_attributes = True

# Order schemas
class OrderBase(BaseModel):
    customer_id: int

class OrderCreate(OrderBase):
    items: List[OrderItemCreate] = []

class OrderUpdate(OrderBase):
    items: List[OrderItemCreate] = []

class Order(OrderBase):
    id: int
    customer: Customer
    items: List[OrderItem] = []
    
    class Config:
        from_attributes = True
