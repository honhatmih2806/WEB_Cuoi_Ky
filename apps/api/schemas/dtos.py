from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, EmailStr

# Base & Reference Schemas
class BrandDTO(BaseModel):
    id: str
    name: str
    slug: str
    logo_url: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True

class CategoryDTO(BaseModel):
    id: str
    name: str
    slug: str
    description: Optional[str] = None
    icon: Optional[str] = None
    product_count: int = 0

    class Config:
        from_attributes = True

class SpecificationDTO(BaseModel):
    id: Optional[str] = None
    spec_group: str
    spec_key: str
    spec_value: str
    order_index: int = 0

    class Config:
        from_attributes = True

class ReviewDTO(BaseModel):
    id: str
    author_name: str
    rating: int
    comment: str
    verified_purchase: bool
    created_at: str

    class Config:
        from_attributes = True

# Product Schemas
class ProductListItemDTO(BaseModel):
    id: str
    title: str
    slug: str
    sku: str
    price: int
    original_price: int
    discount_percent: int
    thumbnail: str
    brief_desc: Optional[str] = None
    stock: int
    rating: float
    review_count: int
    is_featured: bool
    is_bundle: bool
    badge: Optional[str] = None
    brand_name: Optional[str] = None
    category_name: Optional[str] = None
    key_specs: Dict[str, str] = {}

    class Config:
        from_attributes = True

class ProductDetailDTO(ProductListItemDTO):
    gallery: List[str] = []
    full_desc: Optional[str] = None
    specifications: List[SpecificationDTO] = []
    reviews: List[ReviewDTO] = []
    bundle_components: List[ProductListItemDTO] = []

    class Config:
        from_attributes = True

# Cart & Order Schemas
class CartItemInput(BaseModel):
    product_id: str
    quantity: int = Field(default=1, ge=1)

class CheckoutInput(BaseModel):
    customer_name: str = Field(..., min_length=2)
    customer_email: EmailStr
    customer_phone: str = Field(..., min_length=9)
    shipping_address: str = Field(..., min_length=5)
    payment_method: str = Field(default="COD") # COD, BANKING_QR, INSTALLMENT_0
    voucher_code: Optional[str] = None
    notes: Optional[str] = None
    items: List[CartItemInput] = Field(..., min_items=1)

class OrderItemDTO(BaseModel):
    id: str
    product_id: Optional[str]
    product_title: str
    product_sku: str
    unit_price: int
    quantity: int
    subtotal: int

    class Config:
        from_attributes = True

class OrderDTO(BaseModel):
    id: str
    order_code: str
    customer_name: str
    customer_email: str
    customer_phone: str
    shipping_address: str
    payment_method: str
    order_status: str
    total_amount: int
    discount_amount: int
    final_amount: int
    voucher_code: Optional[str] = None
    notes: Optional[str] = None
    created_at: str
    items: List[OrderItemDTO] = []

    class Config:
        from_attributes = True

# AI Synergy Advisor Schemas
class AdvisorRequest(BaseModel):
    use_case: str = Field(default="DEEP_LEARNING") # DEEP_LEARNING, 4K_PRORES_CINEMA, GAMING_STREAMING, MOBILE_EDGE_AI
    budget_range: str = Field(default="HIGH")       # MID, HIGH, ULTRA
    primary_focus: str = Field(default="BOTH")      # IPHONE, NVIDIA, BOTH

class AdvisorRecommendationDTO(BaseModel):
    title: str
    subtitle: str
    matched_iphone: Optional[ProductListItemDTO] = None
    matched_nvidia: Optional[ProductListItemDTO] = None
    synergy_bundle: Optional[ProductListItemDTO] = None
    synergy_reason: str
    benchmark_scores: Dict[str, Any]
    total_savings_vnd: int
