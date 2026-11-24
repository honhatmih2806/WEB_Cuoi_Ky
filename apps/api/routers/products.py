from typing import Optional, List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from core.database import get_db
from core.envelope import ApiResponse, MetaPagination
from core.exceptions import AppException
from models.entities import Product, Brand, Category, ProductSpecification
from schemas.dtos import ProductListItemDTO, ProductDetailDTO, SpecificationDTO, ReviewDTO

router = APIRouter(prefix="/products", tags=["Products"])

def format_product_list_item(p: Product) -> ProductListItemDTO:
    # Extract 2-3 key specs for fast badge display
    key_specs = {}
    if p.specifications:
        for spec in p.specifications[:4]:
            key_specs[spec.spec_key] = spec.spec_value

    return ProductListItemDTO(
        id=p.id,
        title=p.title,
        slug=p.slug,
        sku=p.sku,
        price=p.price,
        original_price=p.original_price,
        discount_percent=p.discount_percent,
        thumbnail=p.thumbnail,
        brief_desc=p.brief_desc,
        stock=p.stock,
        rating=p.rating,
        review_count=p.review_count,
        is_featured=p.is_featured,
        is_bundle=p.is_bundle,
        badge=p.badge,
        brand_name=p.brand.name if p.brand else None,
        category_name=p.category.name if p.category else None,
        key_specs=key_specs,
    )

@router.get("", response_model=ApiResponse[List[ProductListItemDTO]])
def get_products(
    brand_slug: Optional[str] = Query(None, description="Filter by brand: apple, nvidia, titan-synergy"),
    category_slug: Optional[str] = Query(None, description="Filter by category slug"),
    query: Optional[str] = Query(None, description="Search keyword in title or sku"),
    is_featured: Optional[bool] = Query(None, description="Filter featured products"),
    is_bundle: Optional[bool] = Query(None, description="Filter synergy bundles"),
    min_price: Optional[int] = Query(None, description="Minimum price VND"),
    max_price: Optional[int] = Query(None, description="Maximum price VND"),
    sort_by: str = Query("newest", description="Sort: price_asc, price_desc, rating, newest"),
    page: int = Query(1, ge=1),
    page_size: int = Query(24, ge=1, le=100),
    db: Session = Depends(get_db)
):
    q = db.query(Product)

    if brand_slug:
        q = q.join(Product.brand).filter(Brand.slug == brand_slug)
    
    if category_slug:
        q = q.join(Product.category).filter(Category.slug == category_slug)

    if is_featured is not None:
        q = q.filter(Product.is_featured == is_featured)

    if is_bundle is not None:
        q = q.filter(Product.is_bundle == is_bundle)

    if min_price is not None:
        q = q.filter(Product.price >= min_price)

    if max_price is not None:
        q = q.filter(Product.price <= max_price)

    if query:
        search = f"%{query}%"
        q = q.filter(or_(Product.title.ilike(search), Product.sku.ilike(search), Product.brief_desc.ilike(search)))

    # Sorting
    if sort_by == "price_asc":
        q = q.order_by(Product.price.asc())
    elif sort_by == "price_desc":
        q = q.order_by(Product.price.desc())
    elif sort_by == "rating":
        q = q.order_by(Product.rating.desc(), Product.review_count.desc())
    else:
        q = q.order_by(Product.created_at.desc())

    total = q.count()
    items = q.offset((page - 1) * page_size).limit(page_size).all()

    dto_list = [format_product_list_item(p) for p in items]
    return ApiResponse.ok(
        data=dto_list,
        meta=MetaPagination(total=total, page=page, page_size=page_size)
    )

@router.get("/featured", response_model=ApiResponse[List[ProductListItemDTO]])
def get_featured_products(limit: int = 8, db: Session = Depends(get_db)):
    products = db.query(Product).filter(Product.is_featured == True).order_by(Product.rating.desc()).limit(limit).all()
    dto_list = [format_product_list_item(p) for p in products]
    return ApiResponse.ok(data=dto_list)

@router.get("/{slug}", response_model=ApiResponse[ProductDetailDTO])
def get_product_by_slug(slug: str, db: Session = Depends(get_db)):
    p = db.query(Product).filter(Product.slug == slug).first()
    if not p:
        raise AppException(code="ERR_PROD_001", message="Không tìm thấy sản phẩm yêu cầu", status_code=404, details={"slug": slug})

    specs_dto = [
        SpecificationDTO(
            id=s.id,
            spec_group=s.spec_group,
            spec_key=s.spec_key,
            spec_value=s.spec_value,
            order_index=s.order_index
        ) for s in p.specifications
    ]

    reviews_dto = [
        ReviewDTO(
            id=r.id,
            author_name=r.author_name,
            rating=r.rating,
            comment=r.comment,
            verified_purchase=r.verified_purchase,
            created_at=r.created_at.strftime("%d/%m/%Y")
        ) for r in p.reviews
    ]

    components_dto = []
    if p.is_bundle and p.bundle_items:
        for b_item in p.bundle_items:
            if b_item.item:
                components_dto.append(format_product_list_item(b_item.item))

    key_specs = {s.spec_key: s.spec_value for s in p.specifications[:5]}

    detail = ProductDetailDTO(
        id=p.id,
        title=p.title,
        slug=p.slug,
        sku=p.sku,
        price=p.price,
        original_price=p.original_price,
        discount_percent=p.discount_percent,
        thumbnail=p.thumbnail,
        gallery=p.gallery or [p.thumbnail],
        brief_desc=p.brief_desc,
        full_desc=p.full_desc,
        stock=p.stock,
        rating=p.rating,
        review_count=p.review_count,
        is_featured=p.is_featured,
        is_bundle=p.is_bundle,
        badge=p.badge,
        brand_name=p.brand.name if p.brand else None,
        category_name=p.category.name if p.category else None,
        key_specs=key_specs,
        specifications=specs_dto,
        reviews=reviews_dto,
        bundle_components=components_dto
    )
    return ApiResponse.ok(data=detail)
