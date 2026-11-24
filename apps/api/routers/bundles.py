from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from core.envelope import ApiResponse
from models.entities import Product
from schemas.dtos import ProductListItemDTO
from routers.products import format_product_list_item

router = APIRouter(prefix="/bundles", tags=["Synergy Bundles"])

@router.get("", response_model=ApiResponse[List[ProductListItemDTO]])
def get_synergy_bundles(db: Session = Depends(get_db)):
    bundles = db.query(Product).filter(Product.is_bundle == True).all()
    results = [format_product_list_item(b) for b in bundles]
    return ApiResponse.ok(data=results)
