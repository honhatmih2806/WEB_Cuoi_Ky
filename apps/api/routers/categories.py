from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from core.database import get_db
from core.envelope import ApiResponse
from models.entities import Category, Brand, Product
from schemas.dtos import CategoryDTO, BrandDTO

router = APIRouter(tags=["Categories & Brands"])

@router.get("/categories", response_model=ApiResponse[List[CategoryDTO]])
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    results = []
    for c in categories:
        count = db.query(func.count(Product.id)).filter(Product.category_id == c.id).scalar() or 0
        results.append(
            CategoryDTO(
                id=c.id,
                name=c.name,
                slug=c.slug,
                description=c.description,
                icon=c.icon,
                product_count=count
            )
        )
    return ApiResponse.ok(data=results)

@router.get("/brands", response_model=ApiResponse[List[BrandDTO]])
def get_brands(db: Session = Depends(get_db)):
    brands = db.query(Brand).all()
    results = [
        BrandDTO(
            id=b.id,
            name=b.name,
            slug=b.slug,
            logo_url=b.logo_url,
            description=b.description
        )
        for b in brands
    ]
    return ApiResponse.ok(data=results)
