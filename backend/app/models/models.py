from sqlalchemy import Column, Integer, String, Text, ForeignKey, DECIMAL, DateTime, Enum, Table
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from ..database.session import Base

# --------------------
# Enums
# --------------------
class UserRole(str, enum.Enum):
    customer = "customer"
    shopkeeper = "shopkeeper"
    admin = "admin"

class OrderStatus(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"

# --------------------
# Many-to-many table
# --------------------
product_attributes = Table(
    'product_attributes', Base.metadata,
    Column('product_id', Integer, ForeignKey('products.id')),
    Column('attribute_id', Integer, ForeignKey('attributes.id'))
)

# --------------------
# User Table
# --------------------
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.customer)
    created_at = Column(DateTime, default=datetime.utcnow)

    shops = relationship("Shop", back_populates="owner",cascade="all,delete-orphan")
    orders = relationship("Order", back_populates="customer")
    reviews = relationship("Review", back_populates="customer")

# --------------------
# Shop Table
# --------------------
class Shop(Base):
    __tablename__ = "shops"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"), nullable=False)
    shop_name = Column(String(200), nullable=False)
    phone = Column(String(20))
    location_lat = Column(DECIMAL(9,6))
    location_lon = Column(DECIMAL(9,6))
    address = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="shops")
    products = relationship("Product", back_populates="shop",cascade="all,delete-orphan")
    orders = relationship("Order", back_populates="shop")

# --------------------
# Category Table
# --------------------
class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, unique=True)
    description = Column(Text)

    products = relationship("Product", back_populates="category", cascade="all,delete-orphan")

# --------------------
# Attribute Table
# --------------------
class Attribute(Base):
    __tablename__ = "attributes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    value = Column(String(100), nullable=False, unique=True)

    products = relationship('Product', secondary=product_attributes, back_populates="attributes")

# --------------------
# Product Table
# --------------------
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    shop_id = Column(Integer, ForeignKey("shops.id",ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id',ondelete="CASCADE"), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    price = Column(DECIMAL(10,2), nullable=True)
    sales_price =Column(DECIMAL(10,2),nullable=True)
    quantity= Column(Integer, default=0)
    image_url = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    shop = relationship("Shop", back_populates="products")
    category = relationship("Category", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")
    recommendations = relationship("Recommendation", foreign_keys="[Recommendation.product_id]", back_populates="product")
    reviews = relationship("Review", back_populates="product")
    attributes = relationship("Attribute", secondary=product_attributes, back_populates="products")

# --------------------
# Order Table
# --------------------
class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    shop_id = Column(Integer, ForeignKey("shops.id"), nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.pending)
    created_at = Column(DateTime, default=datetime.utcnow)

    customer = relationship("User", back_populates="orders")
    shop = relationship("Shop", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")

    def total_price(self):
        return sum(item.price * item.quantity for item in self.items)
# --------------------
# OrderItem Table
# --------------------
class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False)
    price = Column(DECIMAL(10,2), nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
    
    
    
    

# --------------------
# Recommendation Table
# --------------------
class Recommendation(Base):
    __tablename__ = "recommendations"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    recommended_product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

    product = relationship("Product", foreign_keys=[product_id], back_populates="recommendations")
    recommended_product = relationship("Product", foreign_keys=[recommended_product_id])

# --------------------
# Review Table
# --------------------
class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    rating = Column(Integer)
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    customer = relationship("User", back_populates="reviews")
    product = relationship("Product", back_populates="reviews")
