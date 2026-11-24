import os
import sys

# Add apps/api to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "apps", "api")))

from core.database import engine, Base
from models.entities import Brand, Category, Product, ProductSpecification, BundleItem, Order, OrderItem, Review
from sqlalchemy import text

def init_database():
    print("⏳ [init_db] Đang kiểm tra cấu hình CSDL...")
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1;"))
            conn.commit()
            print("✅ Kết nối cơ sở dữ liệu thành công!")
    except Exception as e:
        print(f"ℹ️ Lưu ý kết nối DB: {e}")

    print("⏳ [init_db] Đang khởi tạo các bảng CSDL...")
    Base.metadata.create_all(bind=engine)
    print("✅ Toàn bộ cấu trúc bảng (brands, categories, products, product_specs, bundle_items, orders, order_items, reviews) đã sẵn sàng!")

if __name__ == "__main__":
    init_database()
