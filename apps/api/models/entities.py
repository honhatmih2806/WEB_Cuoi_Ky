import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Text, Boolean, Integer, BigInteger, Float, DateTime, ForeignKey, JSON
)
from sqlalchemy.orm import relationship
from core.database import Base

def generate_uuid() -> str:
    return str(uuid.uuid4())

class Brand(Base):
    __tablename__ = "brands"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    logo_url = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)

    products = relationship("Product", back_populates="brand", cascade="all, delete-orphan")


class Category(Base):
    __tablename__ = "categories"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    icon = Column(String(50), nullable=True)

    products = relationship("Product", back_populates="category", cascade="all, delete-orphan")


class Product(Base):
    __tablename__ = "products"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    brand_id = Column(String(36), ForeignKey("brands.id", ondelete="SET NULL"), nullable=True)
    category_id = Column(String(36), ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    
    title = Column(String(255), nullable=False, index=True)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    sku = Column(String(64), unique=True, nullable=False)
    
    price = Column(BigInteger, nullable=False)              # Giá bán thực tế (VND)
    original_price = Column(BigInteger, nullable=False)     # Giá niêm yết (VND)
    discount_percent = Column(Integer, default=0)
    
    thumbnail = Column(String(500), nullable=False)
    gallery = Column(JSON, default=list)                   # Danh sách ảnh phụ
    brief_desc = Column(Text, nullable=True)
    full_desc = Column(Text, nullable=True)
    
    stock = Column(Integer, default=10)
    rating = Column(Float, default=5.0)
    review_count = Column(Integer, default=0)
    
    is_featured = Column(Boolean, default=False)
    is_bundle = Column(Boolean, default=False)
    badge = Column(String(50), nullable=True)               # e.g., "HOT", "NEW", "AI TOP", "TIẾT KIỆM 12%"
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    brand = relationship("Brand", back_populates="products")
    category = relationship("Category", back_populates="products")
    specifications = relationship("ProductSpecification", back_populates="product", cascade="all, delete-orphan", order_by="ProductSpecification.order_index")
    reviews = relationship("Review", back_populates="product", cascade="all, delete-orphan")
    bundle_items = relationship("BundleItem", foreign_keys="BundleItem.bundle_product_id", back_populates="bundle", cascade="all, delete-orphan")


class ProductSpecification(Base):
    __tablename__ = "product_specs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    product_id = Column(String(36), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    spec_group = Column(String(100), nullable=False)       # Hiệu năng, Màn hình, AI & Đồ họa...
    spec_key = Column(String(100), nullable=False)         # Chip, VRAM, CUDA...
    spec_value = Column(String(255), nullable=False)       # A18 Pro, 24GB GDDR6X...
    order_index = Column(Integer, default=0)

    product = relationship("Product", back_populates="specifications")


class BundleItem(Base):
    __tablename__ = "bundle_items"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    bundle_product_id = Column(String(36), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    item_product_id = Column(String(36), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, default=1)

    bundle = relationship("Product", foreign_keys=[bundle_product_id], back_populates="bundle_items")
    item = relationship("Product", foreign_keys=[item_product_id])


class Order(Base):
    __tablename__ = "orders"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    order_code = Column(String(50), unique=True, nullable=False, index=True)
    customer_name = Column(String(150), nullable=False)
    customer_email = Column(String(255), nullable=False)
    customer_phone = Column(String(30), nullable=False)
    shipping_address = Column(Text, nullable=False)
    
    payment_method = Column(String(50), default="COD")     # COD, BANKING_QR, INSTALLMENT_0
    order_status = Column(String(50), default="PENDING")   # PENDING, PROCESSING, SHIPPED, DELIVERED
    
    total_amount = Column(BigInteger, nullable=False)
    discount_amount = Column(BigInteger, default=0)
    final_amount = Column(BigInteger, nullable=False)
    voucher_code = Column(String(50), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    order_id = Column(String(36), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(String(36), ForeignKey("products.id", ondelete="SET NULL"), nullable=True)
    
    product_title = Column(String(255), nullable=False)
    product_sku = Column(String(64), nullable=False)
    unit_price = Column(BigInteger, nullable=False)
    quantity = Column(Integer, default=1)
    subtotal = Column(BigInteger, nullable=False)

    order = relationship("Order", back_populates="items")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    product_id = Column(String(36), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    author_name = Column(String(100), nullable=False)
    rating = Column(Integer, default=5)
    comment = Column(Text, nullable=False)
    verified_purchase = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="reviews")
