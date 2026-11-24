import random
from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from core.envelope import ApiResponse
from core.exceptions import AppException
from models.entities import Order, OrderItem, Product
from schemas.dtos import CheckoutInput, OrderDTO, OrderItemDTO

router = APIRouter(prefix="/orders", tags=["Orders"])

def format_order_dto(order: Order) -> OrderDTO:
    items_dto = [
        OrderItemDTO(
            id=i.id,
            product_id=i.product_id,
            product_title=i.product_title,
            product_sku=i.product_sku,
            unit_price=i.unit_price,
            quantity=i.quantity,
            subtotal=i.subtotal
        ) for i in order.items
    ]
    return OrderDTO(
        id=order.id,
        order_code=order.order_code,
        customer_name=order.customer_name,
        customer_email=order.customer_email,
        customer_phone=order.customer_phone,
        shipping_address=order.shipping_address,
        payment_method=order.payment_method,
        order_status=order.order_status,
        total_amount=order.total_amount,
        discount_amount=order.discount_amount,
        final_amount=order.final_amount,
        voucher_code=order.voucher_code,
        notes=order.notes,
        created_at=order.created_at.strftime("%d/%m/%Y %H:%M"),
        items=items_dto
    )

@router.post("/checkout", response_model=ApiResponse[OrderDTO], status_code=201)
def checkout(payload: CheckoutInput, db: Session = Depends(get_db)):
    if not payload.items:
        raise AppException(code="ERR_CART_001", message="Giỏ hàng trống", status_code=400)

    total_amount = 0
    order_items_to_create = []

    for item in payload.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise AppException(code="ERR_PROD_001", message=f"Không tìm thấy sản phẩm {item.product_id}", status_code=404)
        
        if product.stock < item.quantity:
            raise AppException(code="ERR_CART_002", message=f"Sản phẩm {product.title} không đủ tồn kho (còn {product.stock})", status_code=400)

        subtotal = product.price * item.quantity
        total_amount += subtotal

        # Giảm tồn kho
        product.stock -= item.quantity

        order_items_to_create.append({
            "product": product,
            "quantity": item.quantity,
            "unit_price": product.price,
            "subtotal": subtotal
        })

    # Tính toán giảm giá theo Voucher
    discount_amount = 0
    voucher_code_applied = None
    if payload.voucher_code:
        code_clean = payload.voucher_code.strip().upper()
        if code_clean in ("UTEVIP", "TITANVIP"):
            discount_amount = min(int(total_amount * 0.05), 2000000)
            voucher_code_applied = f"{code_clean} (Giảm 5%)"
        elif code_clean in ("LUXURY", "SYNERGY"):
            discount_amount = min(int(total_amount * 0.10), 5000000)
            voucher_code_applied = f"{code_clean} (Giảm 10%)"
        elif code_clean in ("UTETECHSTORE", "APPLE2026"):
            if total_amount >= 20000000:
                discount_amount = 1000000
                voucher_code_applied = f"{code_clean} (Giảm 1.000.000đ)"
        else:
            raise AppException(code="ERR_VOC_001", message="Mã giảm giá không hợp lệ hoặc đã hết hạn", status_code=400)

    final_amount = max(0, total_amount - discount_amount)
    order_code = f"ORD-2026-{random.randint(10000, 99999)}"

    order = Order(
        order_code=order_code,
        customer_name=payload.customer_name,
        customer_email=payload.customer_email,
        customer_phone=payload.customer_phone,
        shipping_address=payload.shipping_address,
        payment_method=payload.payment_method,
        order_status="PROCESSING",
        total_amount=total_amount,
        discount_amount=discount_amount,
        final_amount=final_amount,
        voucher_code=voucher_code_applied,
        notes=payload.notes,
        created_at=datetime.utcnow()
    )
    db.add(order)
    db.flush()

    for item_data in order_items_to_create:
        p = item_data["product"]
        oi = OrderItem(
            order_id=order.id,
            product_id=p.id,
            product_title=p.title,
            product_sku=p.sku,
            unit_price=item_data["unit_price"],
            quantity=item_data["quantity"],
            subtotal=item_data["subtotal"]
        )
        db.add(oi)

    db.commit()
    db.refresh(order)

    return ApiResponse.ok(data=format_order_dto(order))

@router.get("/track/{order_code}", response_model=ApiResponse[OrderDTO])
def track_order(order_code: str, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.order_code == order_code.strip().upper()).first()
    if not order:
        raise AppException(code="ERR_ORD_001", message=f"Không tìm thấy đơn hàng mã {order_code}", status_code=404)
    return ApiResponse.ok(data=format_order_dto(order))

@router.get("", response_model=ApiResponse[List[OrderDTO]])
def list_orders(limit: int = 10, db: Session = Depends(get_db)):
    orders = db.query(Order).order_by(Order.created_at.desc()).limit(limit).all()
    return ApiResponse.ok(data=[format_order_dto(o) for o in orders])
