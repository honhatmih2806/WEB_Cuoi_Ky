import os
import sys
import uuid
from datetime import datetime

# Disable Cython C-extension for SQLAlchemy compatibility on Windows
os.environ["DISABLE_SQLALCHEMY_CEXT"] = "1"

# Add apps/api to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "apps", "api")))

from core.database import SessionLocal, engine, Base
from models.entities import Brand, Category, Product, ProductSpecification, BundleItem, Review

def seed():
    print("🌱 [seed_products] Khởi tạo CSDL siêu thị điện tử cao cấp Titan TechStore...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Xóa dữ liệu cũ
        db.query(BundleItem).delete()
        db.query(Review).delete()
        db.query(ProductSpecification).delete()
        db.query(Product).delete()
        db.query(Category).delete()
        db.query(Brand).delete()
        db.commit()

        # 1. BRANDS (Thương hiệu điện tử hàng đầu thế giới)
        brands_data = [
            ("apple", "Apple", "Tập đoàn công nghệ hàng đầu thế giới với hệ sinh thái iPhone, Mac, iPad và vi xử lý Apple Silicon."),
            ("nvidia", "NVIDIA", "Tập đoàn điện toán tối thượng và trí tuệ nhân tạo toàn cầu, chủ nhân dòng GPU GeForce RTX và vi máy tính Jetson."),
            ("sony", "Sony", "Thương hiệu điện tử Nhật Bản huyền thoại với chuẩn âm thanh Hi-Res, máy chơi game PlayStation và cảm biến máy ảnh."),
            ("samsung", "Samsung", "Tập đoàn công nghệ số một Hàn Quốc với dòng smartphone Galaxy Ultra, màn hình OLED và giải pháp lưu trữ."),
            ("dell", "Dell Technologies", "Nhà sản xuất máy trạm và máy tính xách tay doanh nhân cao cấp Dell XPS và màn hình đồ họa UltraSharp."),
            ("asus", "ASUS ROG & ProArt", "Thương hiệu phần cứng máy tính gaming và sáng tạo nghệ thuật đồ họa hàng đầu thế giới."),
            ("lenovo", "Lenovo ThinkPad", "Dòng máy tính xách tay văn phòng và máy trạm di động siêu bền bỉ chuẩn quân đội."),
            ("google", "Google Pixel", "Dòng điện thoại thông minh thuần Android và trí tuệ nhân tạo Gemini tích hợp sâu."),
            ("bang-olufsen", "Bang & Olufsen", "Thương hiệu âm thanh xa xỉ Đan Mạch với thiết kế nhôm nguyên khối và chất âm acoustic chuẩn phòng thu."),
            ("nintendo", "Nintendo", "Biểu tượng máy chơi game gia đình và thiết bị giải trí tương tác toàn cầu từ Kyoto, Nhật Bản."),
            ("logitech-keychron", "Logitech & Keychron", "Thương hiệu thiết bị ngoại vi, bàn phím cơ nhôm CNC và chuột công thái học cao cấp."),
            ("titan-synergy", "Titan Synergy Studio", "Giải pháp phần cứng tích hợp độc quyền kết hợp giữa di động cao cấp và trạm xử lý AI.")
        ]

        brand_map = {}
        for slug, name, desc in brands_data:
            b = Brand(
                id=str(uuid.uuid4()),
                name=name,
                slug=slug,
                logo_url=f"https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=300&auto=format&fit=crop&q=80",
                description=desc
            )
            db.add(b)
            brand_map[slug] = b
        db.commit()

        # 2. CATEGORIES (Danh mục sản phẩm điện tử đầy đủ)
        categories_data = [
            ("laptops", "Máy Tính Xách Tay (Laptops & MacBooks)", "MacBook Pro, Dell XPS, ASUS ROG, ThinkPad cho lập trình và đồ họa chuyên nghiệp."),
            ("smartphones", "Điện Thoại Di Động Flagship", "iPhone 16 Pro Max, Samsung Galaxy S24 Ultra, Google Pixel với camera điện ảnh."),
            ("tablets", "Máy Tính Bảng (Tablets & iPads)", "iPad Pro M4 Tandem OLED, Galaxy Tab S9 Ultra phục vụ vẽ phác thảo và đa nhiệm."),
            ("audio", "Thiết Bị Âm Thanh & Tai Nghe Hi-Fi", "AirPods Max, Sony WH-1000XM5, Bang & Olufsen với khả năng chống ồn chủ động cao cấp."),
            ("smartwatches", "Đồng Hồ Thông Minh & Wearables", "Apple Watch Ultra 2, Galaxy Watch, Garmin đo lường thể thao và sức khỏe chuyên sâu."),
            ("monitors", "Màn Hình Đồ Họa & Gaming", "Apple Studio Display 5K, Dell UltraSharp 6K, LG OLED 4K chuẩn màu thiết kế."),
            ("pc-components", "Linh Kiện Máy Tính & AI Trạm", "NVIDIA RTX 5090/4090, CPU Intel Core Ultra, AMD Ryzen 9, Jetson Orin AI Edge."),
            ("consoles", "Máy Chơi Game & Thiết Bị Giải Trí", "PlayStation 5 Pro, Nintendo Switch OLED, Steam Deck cho trải nghiệm giải trí hoàn hảo."),
            ("accessories", "Phụ Kiện Điện Tử Cao Cấp", "Cáp Thunderbolt 5 Pro, sạc nhanh GaN 240W, bàn phím cơ nhôm CNC và chuột không dây."),
            ("bundles", "Gói Giải Pháp Sáng Tạo & AI", "Combo phần cứng tối ưu hóa công việc giữa điện thoại flagship và card đồ họa máy trạm.")
        ]

        category_map = {}
        for slug, name, desc in categories_data:
            c = Category(
                id=str(uuid.uuid4()),
                name=name,
                slug=slug,
                description=desc,
                icon=slug
            )
            db.add(c)
            category_map[slug] = c
        db.commit()

        # 3. COMPREHENSIVE ELECTRONICS CATALOG
        products_list = [
            # --- LAPTOPS & MACBOOKS ---
            {
                "title": "Apple MacBook Pro 16\" M4 Max (48GB Unified RAM, 1TB SSD, Space Black)",
                "slug": "macbook-pro-16-m4-max-48gb-1tb-space-black",
                "sku": "APL-MBP16-M4MAX-48G",
                "brand_slug": "apple",
                "category_slug": "laptops",
                "price": 89990000,
                "original_price": 94990000,
                "discount_percent": 5,
                "thumbnail": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=800&auto=format&fit=crop&q=80",
                "gallery": [
                    "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=800&auto=format&fit=crop&q=80",
                    "https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?w=800&auto=format&fit=crop&q=80"
                ],
                "brief_desc": "Chip Apple M4 Max 16-core CPU và 40-core GPU, Màn hình 16.2\" Liquid Retina XDR 120Hz ProMotion độ sáng 1600 nits, Thời lượng pin 24 giờ liên tục.",
                "full_desc": "MacBook Pro 16 inch với chip M4 Max là cỗ máy điện toán xách tay mạnh mẽ nhất dành cho nhà phát triển phần mềm, đạo diễn dựng phim 8K và kỹ sư huấn luyện mô hình học máy. Vỏ nhôm nguyên khối Space Black anode hóa chống bám vân tay.",
                "stock": 12,
                "rating": 4.98,
                "review_count": 86,
                "is_featured": True,
                "badge": "APPLE M4 MAX",
                "specs": [
                    ("Hiệu Năng", "Vi xử lý", "Apple M4 Max (16 nhân CPU, 40 nhân GPU, 16 nhân Neural Engine)"),
                    ("Bộ Nhớ", "Unified Memory", "48GB bộ nhớ thống nhất tốc độ 546GB/s"),
                    ("Lưu Trữ", "Dung lượng ổ cứng", "1TB SSD NVMe tốc độ 7.4 GB/s"),
                    ("Màn Hình", "Kích thước & Tấm nền", "16.2 inch Liquid Retina XDR (3456 x 2234), 120Hz ProMotion"),
                    ("Cổng Kết Nối", "Giao tiếp", "3x Thunderbolt 5 (120Gbps), HDMI 2.1 8K, Khe thẻ SDXC, MagSafe 3")
                ]
            },
            {
                "title": "Apple MacBook Air 15\" M3 (16GB RAM, 512GB SSD, Midnight)",
                "slug": "macbook-air-15-m3-16gb-512gb-midnight",
                "sku": "APL-MBA15-M3-16G",
                "brand_slug": "apple",
                "category_slug": "laptops",
                "price": 37990000,
                "original_price": 40990000,
                "discount_percent": 7,
                "thumbnail": "https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?w=800&auto=format&fit=crop&q=80",
                "gallery": [
                    "https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?w=800&auto=format&fit=crop&q=80"
                ],
                "brief_desc": "Mỏng nhẹ chỉ 11.5mm, Chip Apple M3 tiến trình 3nm, Màn hình Liquid Retina 15.3 inch 500 nits, Thiết kế không quạt tản nhiệt hoàn toàn yên tĩnh.",
                "full_desc": "MacBook Air 15 inch M3 mang đến không gian làm việc rộng rãi trong thân hình siêu mỏng. Hỗ trợ xuất 2 màn hình ngoài khi gập máy, âm thanh 6 loa vòm Spatial Audio và thời lượng pin ấn tượng lên tới 18 tiếng.",
                "stock": 20,
                "rating": 4.92,
                "review_count": 115,
                "is_featured": False,
                "badge": "MỎNG NHẸ 11.5MM",
                "specs": [
                    ("Hiệu Năng", "Vi xử lý", "Apple M3 (8 nhân CPU, 10 nhân GPU)"),
                    ("Bộ Nhớ", "RAM", "16GB Unified Memory"),
                    ("Lưu Trữ", "SSD", "512GB NVMe siêu tốc"),
                    ("Màn Hình", "Hiển thị", "15.3 inch Liquid Retina 2880 x 1864, True Tone"),
                    ("Trọng Lượng", "Khối lượng", "1.51 kg")
                ]
            },
            {
                "title": "Dell XPS 16 9640 (Intel Core Ultra 9 185H, RTX 4070 8GB, 32GB RAM, 4K+ OLED Touch)",
                "slug": "dell-xps-16-9640-core-ultra-9-rtx-4070-oled",
                "sku": "DEL-XPS16-U9-4070",
                "brand_slug": "dell",
                "category_slug": "laptops",
                "price": 78990000,
                "original_price": 84990000,
                "discount_percent": 7,
                "thumbnail": "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=800&auto=format&fit=crop&q=80",
                "gallery": [
                    "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=800&auto=format&fit=crop&q=80"
                ],
                "brief_desc": "Khung nhôm CNC gia công tinh xảo, Mặt kính Gorilla Glass Victus cảm ứng xúc giác liền mạch, Màn hình 4K+ OLED 120Hz 100% DCI-P3, GPU NVIDIA RTX 4070 Studio.",
                "full_desc": "Kiệt tác thiết kế laptop Windows tối giản và sang trọng nhất hiện nay. Hàng phím chức năng cảm ứng vô hình và touchpad tích hợp rung haptic trên mặt kính phẳng tuyệt đối.",
                "stock": 8,
                "rating": 4.95,
                "review_count": 48,
                "is_featured": True,
                "badge": "CHUẨN DOANH NHÂN",
                "specs": [
                    ("Hiệu Năng", "Bộ xử lý CPU", "Intel Core Ultra 9 185H (16 nhân 22 luồng, NPU AI tích hợp)"),
                    ("Đồ Họa", "Card đồ họa rời", "NVIDIA GeForce RTX 4070 8GB GDDR6 (NVIDIA Studio Drivers)"),
                    ("Bộ Nhớ", "RAM & SSD", "32GB LPDDR5x 7467MHz + 1TB PCIe Gen 4 SSD"),
                    ("Màn Hình", "Tấm nền", "16.3\" 4K+ OLED (3840 x 2400) Touch, 120Hz, 100% DCI-P3"),
                    ("Chất Liệu", "Khung máy", "Nhôm Platinum gia công CNC nguyên khối")
                ]
            },
            {
                "title": "ASUS ROG Zephyrus G16 (Core Ultra 9 185H, RTX 4080 12GB, 32GB RAM, ROG Nebula OLED 240Hz)",
                "slug": "asus-rog-zephyrus-g16-rtx-4080-nebula-oled",
                "sku": "ASU-ROG-G16-4080",
                "brand_slug": "asus",
                "category_slug": "laptops",
                "price": 74990000,
                "original_price": 79990000,
                "discount_percent": 6,
                "thumbnail": "https://images.unsplash.com/photo-1544717305-2782549b5136?w=800&auto=format&fit=crop&q=80",
                "gallery": [
                    "https://images.unsplash.com/photo-1544717305-2782549b5136?w=800&auto=format&fit=crop&q=80"
                ],
                "brief_desc": "Khung nhôm CNC siêu mỏng chỉ 1.49cm, Trọng lượng 1.85kg, Dải đèn Slash Lighting tinh tế, Màn hình OLED 2.5K 240Hz chuẩn G-Sync và VESA DisplayHDR True Black 500.",
                "full_desc": "Chiếc laptop kết hợp hoàn hảo giữa độ mỏng nhẹ thanh lịch của ultrabook cao cấp và sức mạnh xử lý đồ họa khủng của dòng gaming đầu bảng.",
                "stock": 10,
                "rating": 4.96,
                "review_count": 62,
                "is_featured": False,
                "badge": "OLED 240HZ 0.2MS",
                "specs": [
                    ("CPU & GPU", "Cấu hình chính", "Intel Core Ultra 9 185H + NVIDIA RTX 4080 12GB GDDR6"),
                    ("Bộ Nhớ", "RAM & SSD", "32GB LPDDR5X-7467 + 2TB NVMe M.2 Gen4"),
                    ("Màn Hình", "ROG Nebula OLED", "16 inch 2.5K (2560 x 1600) OLED 240Hz 0.2ms, G-Sync"),
                    ("Tản Nhiệt", "Công nghệ", "Buồng hơi Vapor Chamber + Kim loại lỏng Thermal Grizzly")
                ]
            },
            {
                "title": "Lenovo ThinkPad X1 Carbon Gen 12 (Core Ultra 7 155H, 32GB RAM, 1TB SSD, 2.8K OLED)",
                "slug": "lenovo-thinkpad-x1-carbon-gen-12-oled",
                "sku": "LEN-X1C12-U7-OLED",
                "brand_slug": "lenovo",
                "category_slug": "laptops",
                "price": 54990000,
                "original_price": 59990000,
                "discount_percent": 8,
                "thumbnail": "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=800&auto=format&fit=crop&q=80",
                "gallery": [
                    "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=800&auto=format&fit=crop&q=80"
                ],
                "brief_desc": "Trọng lượng chỉ 1.09kg chế tác từ sợi carbon tái chế và magie, Bàn phím ThinkPad huyền thoại với nút TrackPoint biểu tượng, Màn hình 14\" 2.8K OLED 120Hz.",
                "full_desc": "Chuẩn mực laptop doanh nhân toàn cầu qua nhiều thập kỷ. Độ bền đạt tiêu chuẩn quân sự Hoa Kỳ MIL-STD 810H, tích hợp chip bảo mật TPM 2.0 và nhận diện khuôn mặt IR Camera.",
                "stock": 15,
                "rating": 4.94,
                "review_count": 73,
                "is_featured": False,
                "badge": "SIÊU BỀN MIL-STD 810H",
                "specs": [
                    ("Hiệu Năng", "Vi xử lý", "Intel Core Ultra 7 155H 16 nhân, Intel Arc Graphics"),
                    ("Trọng Lượng", "Khối lượng thân máy", "1.09 kg (2.42 lbs)"),
                    ("Màn Hình", "Hiển thị", "14 inch 2.8K (2880 x 1800) OLED, 120Hz, DisplayHDR 500"),
                    ("Bảo Mật", "Security", "ThinkShield, Vân tay sinh trắc học, Cần gạt camera vật lý")
                ]
            },

            # --- SMARTPHONES & FLAGSHIPS ---
            {
                "title": "iPhone 16 Pro Max 1TB Titan Sa Mạc (Desert Titanium)",
                "slug": "iphone-16-pro-max-1tb-desert-titanium",
                "sku": "APL-IP16PM-1TB-DES",
                "brand_slug": "apple",
                "category_slug": "smartphones",
                "price": 46990000,
                "original_price": 49990000,
                "discount_percent": 6,
                "thumbnail": "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=800&auto=format&fit=crop&q=80",
                "gallery": [
                    "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=800&auto=format&fit=crop&q=80",
                    "https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=800&auto=format&fit=crop&q=80"
                ],
                "brief_desc": "Màn hình 6.9\" Super Retina XDR ProMotion 120Hz, Chip A18 Pro 3nm, Cụm 3 camera Fusion 48MP zoom quang 5x tetraprism, Quay 4K 120fps Dolby Vision Apple Log.",
                "full_desc": "iPhone 16 Pro Max được chế tác từ Titanium Cấp 5 siêu bền và nhẹ, với viền màn hình mỏng nhất từng có. Nút Camera Control thế hệ mới hỗ trợ truy cập nhanh công cụ chụp và quay phim.",
                "stock": 25,
                "rating": 4.98,
                "review_count": 210,
                "is_featured": True,
                "badge": "FLAGSHIP 2026",
                "specs": [
                    ("Hiệu Năng", "Chipset", "Apple A18 Pro (6 nhân CPU, 6 nhân GPU, 16 nhân NPU)"),
                    ("Bộ Nhớ", "Dung lượng lưu trữ", "1TB NVMe siêu tốc"),
                    ("Màn Hình", "Kích thước & Công nghệ", "6.9 inch Super Retina XDR OLED, 120Hz ProMotion"),
                    ("Camera", "Quay phim điện ảnh", "4K 120fps ProRes, Apple Log, Cảm biến Fusion 48MP"),
                    ("Kết Nối", "Chuẩn sạc & Dữ liệu", "USB-C 3.2 Gen 2 (10Gbps), Wi-Fi 7, MagSafe 25W")
                ]
            },
            {
                "title": "Samsung Galaxy S24 Ultra 512GB Titanium Gray",
                "slug": "samsung-galaxy-s24-ultra-512gb-titanium-gray",
                "sku": "SAM-S24U-512G-GRY",
                "brand_slug": "samsung",
                "category_slug": "smartphones",
                "price": 33990000,
                "original_price": 37490000,
                "discount_percent": 9,
                "thumbnail": "https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=800&auto=format&fit=crop&q=80",
                "gallery": [
                    "https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=800&auto=format&fit=crop&q=80"
                ],
                "brief_desc": "Khung viền Titanium cao cấp, Bút S-Pen tích hợp trong thân máy, Màn hình phẳng 6.8\" Dynamic AMOLED 2X chống chói Corning Gorilla Armor, Camera 200MP zoom 100x Space Zoom.",
                "full_desc": "Smartphone Android đầu bảng tích hợp bộ công cụ trí tuệ nhân tạo Galaxy AI: Khoanh tròn để tìm kiếm (Circle to Search), Phiên dịch cuộc gọi trực tiếp hai chiều và Chỉnh sửa ảnh thông minh Generative Edit.",
                "stock": 18,
                "rating": 4.93,
                "review_count": 140,
                "is_featured": True,
                "badge": "GALAXY AI & S-PEN",
                "specs": [
                    ("Hiệu Năng", "Vi xử lý", "Snapdragon 8 Gen 3 for Galaxy (4nm)"),
                    ("Bộ Nhớ", "RAM & ROM", "12GB RAM LPDDR5X + 512GB UFS 4.0"),
                    ("Màn Hình", "Tấm nền", "6.8\" QHD+ Dynamic AMOLED 2X, 1-120Hz, 2600 nits, Kính chống lóa"),
                    ("Camera", "Hệ thống ống kính", "200MP Wide + 50MP 5x Periscope + 10MP 3x + 12MP Ultra-wide"),
                    ("Pin & Sạc", "Dung lượng pin", "5,000 mAh sạc nhanh 45W có dây, 15W không dây")
                ]
            },
            {
                "title": "Google Pixel 9 Pro XL 256GB Obsidian",
                "slug": "google-pixel-9-pro-xl-256gb-obsidian",
                "sku": "GGL-PIX9PXL-256G",
                "brand_slug": "google",
                "category_slug": "smartphones",
                "price": 28990000,
                "original_price": 31990000,
                "discount_percent": 9,
                "thumbnail": "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=800&auto=format&fit=crop&q=80",
                "gallery": [
                    "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=800&auto=format&fit=crop&q=80"
                ],
                "brief_desc": "Chip Google Tensor G4 tối ưu riêng cho mô hình Gemini Nano đa phương thức, Màn hình Super Actua OLED 6.8\" 3000 nits sáng nhất thế giới smartphone, Thuật toán nhiếp ảnh điện toán số 1.",
                "full_desc": "Thiết kế thanh camera ngang biểu tượng bằng kim loại nhám sang trọng. Cập nhật phần mềm hệ điều hành Android thuần khiết trực tiếp từ Google trong suốt 7 năm liên tục.",
                "stock": 14,
                "rating": 4.91,
                "review_count": 68,
                "is_featured": False,
                "badge": "GEMINI NANO AI",
                "specs": [
                    ("Chipset", "Vi xử lý AI", "Google Tensor G4 + Đồng vi xử lý bảo mật Titan M2"),
                    ("Bộ Nhớ", "RAM & Bộ nhớ", "16GB RAM + 256GB NVMe"),
                    ("Màn Hình", "Super Actua", "6.8\" LTPO OLED (1344 x 2992), 1-120Hz, 3000 nits Peak"),
                    ("Nhiếp Ảnh", "Camera sau", "50MP Octa PD Main + 48MP Quad PD Ultra-wide + 48MP 5x Telephoto"),
                    ("Hệ Điều Hành", "Hỗ trợ phần mềm", "7 năm nâng cấp Android OS, bảo mật và Pixel Drop")
                ]
            },
            {
                "title": "Sony Xperia 1 VI (12GB RAM, 512GB, Khaki Green, Âm Thanh Hi-Res 3.5mm)",
                "slug": "sony-xperia-1-vi-512gb-khaki-green",
                "sku": "SNY-XP1VI-512G-GRN",
                "brand_slug": "sony",
                "category_slug": "smartphones",
                "price": 31990000,
                "original_price": 34990000,
                "discount_percent": 8,
                "thumbnail": "https://images.unsplash.com/photo-1511707171634-5f897ff02560?w=800&auto=format&fit=crop&q=80",
                "gallery": [
                    "https://images.unsplash.com/photo-1511707171634-5f897ff02560?w=800&auto=format&fit=crop&q=80"
                ],
                "brief_desc": "Ống kính quang học zoom liên tục 85-170mm chuẩn máy ảnh Alpha, Cổng tai nghe 3.5mm Hi-Res Audio mạ vàng, Màn hình OLED tỷ lệ 19.5:9 Powered by BRAVIA.",
                "full_desc": "Sản phẩm điện thoại dành riêng cho nhiếp ảnh gia và người đam mê âm thanh audiophile. Tích hợp nút cứng chụp ảnh 2 nấc chuyên dụng và cảm biến Exmor T for mobile 2 tầng bóng bán dẫn.",
                "stock": 11,
                "rating": 4.89,
                "review_count": 42,
                "is_featured": False,
                "badge": "ỐNG KÍNH QUANG HỌC ZEISS",
                "specs": [
                    ("Ống Kính", "Hệ thống zoom", "85mm - 170mm Optical Telephoto Lens chuẩn ZEISS T*"),
                    ("Âm Thanh", "Chuẩn giải mã", "Hi-Res Audio, LDAC, DSEE Ultimate, Giắc 3.5mm analog"),
                    ("Màn Hình", "BRAVIA OLED", "6.5\" FHD+ LTPO 1-120Hz, tỷ lệ 19.5:9 Sunlight Vision"),
                    ("Hiệu Năng", "Cấu hình", "Snapdragon 8 Gen 3, 12GB RAM, 512GB, hỗ trợ thẻ MicroSD 1.5TB")
                ]
            },

            # --- TABLETS & IPADS ---
            {
                "title": "Apple iPad Pro 13\" M4 Ultra Retina Tandem OLED (512GB, Wi-Fi, Space Black)",
                "slug": "ipad-pro-13-m4-tandem-oled-512gb-space-black",
                "sku": "APL-IPP13-M4-512G",
                "brand_slug": "apple",
                "category_slug": "tablets",
                "price": 38990000,
                "original_price": 41990000,
                "discount_percent": 7,
                "thumbnail": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=800&auto=format&fit=crop&q=80",
                "gallery": [
                    "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=800&auto=format&fit=crop&q=80"
                ],
                "brief_desc": "Độ mỏng kỷ lục 5.1mm mỏng nhất lịch sử Apple, Chip Apple M4 thế hệ mới 38 TOPS, Màn hình Ultra Retina XDR Tandem OLED 2 lớp phát xạ sáng 1000 nits toàn màn hình.",
                "full_desc": "Đỉnh cao máy tính bảng sáng tạo. Tương thích hoàn hảo với bút cảm ứng Apple Pencil Pro hỗ trợ xoay thân bút cảm ứng xúc giác (Barrel Roll) và bàn phím Magic Keyboard nhôm nguyên khối.",
                "stock": 16,
                "rating": 4.97,
                "review_count": 94,
                "is_featured": True,
                "badge": "TANDEM OLED 5.1MM",
                "specs": [
                    ("Độ Mỏng & Trọng Lượng", "Kích thước", "Dày 5.1 mm, Nặng 579g"),
                    ("Vi Xử Lý", "Chipset", "Apple M4 (9-core CPU, 10-core GPU, 16-core NPU 38 TOPS)"),
                    ("Màn Hình", "Tấm nền đột phá", "13 inch Tandem OLED (2752 x 2064), 120Hz ProMotion"),
                    ("Phụ Kiện Hỗ Trợ", "Giao tiếp", "Apple Pencil Pro, Magic Keyboard 2024, Thunderbolt 3")
                ]
            },
            {
                "title": "Samsung Galaxy Tab S9 Ultra 512GB (Màn hình 14.6\" Dynamic AMOLED 2X, S-Pen)",
                "slug": "samsung-galaxy-tab-s9-ultra-512gb",
                "sku": "SAM-TABS9U-512G",
                "brand_slug": "samsung",
                "category_slug": "tablets",
                "price": 27990000,
                "original_price": 31990000,
                "discount_percent": 12,
                "thumbnail": "https://images.unsplash.com/photo-1589739900243-4b52cd9b104e?w=800&auto=format&fit=crop&q=80",
                "gallery": [
                    "https://images.unsplash.com/photo-1589739900243-4b52cd9b104e?w=800&auto=format&fit=crop&q=80"
                ],
                "brief_desc": "Màn hình khổng lồ 14.6 inch viền siêu mỏng, Chuẩn kháng nước kháng bụi IP68 toàn diện cho cả thân máy và bút S-Pen, Chế độ máy tính để bàn Samsung DeX.",
                "full_desc": "Thay thế trọn vẹn màn hình phụ di động hoặc laptop văn phòng khi kết hợp bao da bàn phím. Đa nhiệm mở cùng lúc 3 cửa sổ ứng dụng độc lập với độ mượt mà tuyệt hảo.",
                "stock": 12,
                "rating": 4.91,
                "review_count": 55,
                "is_featured": False,
                "badge": "KHÁNG NƯỚC IP68 14.6\"",
                "specs": [
                    ("Màn Hình", "Kích thước khổng lồ", "14.6 inch Dynamic AMOLED 2X 120Hz (2960 x 1848)"),
                    ("Cấu Hình", "Chip & Bộ nhớ", "Snapdragon 8 Gen 2 for Galaxy, 12GB RAM, 512GB SSD"),
                    ("Âm Thanh", "Loa ngoài", "Hệ thống 4 loa AKG kích thước lớn hỗ trợ Dolby Atmos"),
                    ("Độ Bền", "Tiêu chuẩn bảo vệ", "Kháng nước & bụi chuẩn IP68 cao nhất")
                ]
            },

            # --- AUDIO & HEADPHONES ---
            {
                "title": "Apple AirPods Max (USB-C 2026, Space Gray, Âm Thanh Không Gian Cá Nhân Hóa)",
                "slug": "apple-airpods-max-usb-c-space-gray",
                "sku": "APL-APMAX-USBC-GRY",
                "brand_slug": "apple",
                "category_slug": "audio",
                "price": 13990000,
                "original_price": 14990000,
                "discount_percent": 6,
                "thumbnail": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=800&auto=format&fit=crop&q=80",
                "gallery": [
                    "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=800&auto=format&fit=crop&q=80"
                ],
                "brief_desc": "Driver điện động 40mm do Apple chế tạo riêng, Khung vòm lưới thoáng khí thép không gỉ, Khử tiếng ồn chủ động chuyên nghiệp và cổng sạc chuẩn USB-C thế hệ mới.",
                "full_desc": "Tai nghe over-ear cao cấp mang trải nghiệm âm thanh phòng hòa nhạc vào không gian cá nhân. Chip Apple H1 ở mỗi bên chụp tai tính toán âm học thích ứng 9 tỷ lần mỗi giây.",
                "stock": 20,
                "rating": 4.95,
                "review_count": 130,
                "is_featured": True,
                "badge": "CHỐNG ỒN ĐỈNH CAO",
                "specs": [
                    ("Màng Loa", "Driver âm học", "Driver điện động 40mm từ tính neodymium kép"),
                    ("Công Nghệ", "Xử lý âm học", "Active Noise Cancellation (ANC), Transparency Mode, Spatial Audio"),
                    ("Cổng Kết Nối", "Chuẩn sạc", "USB-C sạc nhanh (5 phút nghe 1.5 giờ)"),
                    ("Thời Lượng", "Pin", "Lên đến 20 giờ phát nhạc liên tục với ANC bật")
                ]
            },
            {
                "title": "Sony WH-1000XM5 Hi-Res Noise Canceling Headphones (Black)",
                "slug": "sony-wh-1000xm5-wireless-headphones-black",
                "sku": "SNY-WH1000XM5-BLK",
                "brand_slug": "sony",
                "category_slug": "audio",
                "price": 7990000,
                "original_price": 8990000,
                "discount_percent": 11,
                "thumbnail": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&auto=format&fit=crop&q=80",
                "gallery": [
                    "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&auto=format&fit=crop&q=80"
                ],
                "brief_desc": "Hai vi xử lý điều khiển 8 micro chống ồn tự động tối ưu theo áp suất không khí, Driver màng carbon composite 30mm, Chuẩn mã hóa âm thanh LDAC không dây 990kbps.",
                "full_desc": "Chiếc tai nghe chống ồn không dây hàng đầu được các chuyên gia âm nhạc và hành khách bay toàn cầu tin dùng. Thời lượng pin 30 giờ và trọng lượng siêu nhẹ 250g.",
                "stock": 35,
                "rating": 4.94,
                "review_count": 240,
                "is_featured": False,
                "badge": "HI-RES WIRELESS LDAC",
                "specs": [
                    ("Bộ Xử Lý Chống Ồn", "Dual Processors", "Sony Integrated Processor V1 + HD QN1"),
                    ("Microphone", "Hệ thống mic", "8 microphones đàm thoại khử ồn gió bằng AI"),
                    ("Thời Lượng Pin", "Dung lượng", "30 giờ nghe nhạc ANC bật (40 giờ khi tắt ANC)"),
                    ("Trọng Lượng", "Thiết kế nhẹ", "250g đệm da mềm mại không gây áp lực tai")
                ]
            },
            {
                "title": "Bang & Olufsen Beoplay H95 Luxury ANC Headphones (Nordic Ice Titanium)",
                "slug": "bang-olufsen-beoplay-h95-nordic-ice",
                "sku": "BNO-H95-NORICE",
                "brand_slug": "bang-olufsen",
                "category_slug": "audio",
                "price": 28990000,
                "original_price": 32000000,
                "discount_percent": 9,
                "thumbnail": "https://images.unsplash.com/photo-1583394838336-acd977736f90?w=800&auto=format&fit=crop&q=80",
                "gallery": [
                    "https://images.unsplash.com/photo-1583394838336-acd977736f90?w=800&auto=format&fit=crop&q=80"
                ],
                "brief_desc": "Driver Titanium 40mm điều chỉnh bởi chuyên gia âm học Đan Mạch, Khung nhôm chải xước thủ công kết hợp da cừu tự nhiên siêu mềm, Núm xoay cơ khí xoay điều chỉnh âm lượng chính xác.",
                "full_desc": "Biểu tượng của sự xa xỉ trong thế giới tai nghe hi-end. Đi kèm hộp đựng du lịch bằng nhôm nguyên khối đúc khuôn tùy chỉnh, chất lượng hoàn thiện tiệm cận nghệ thuật kim hoàn.",
                "stock": 6,
                "rating": 5.0,
                "review_count": 28,
                "is_featured": True,
                "badge": "XA XỈ ĐAN MẠCH",
                "specs": [
                    ("Chất Liệu Chế Tác", "Vật liệu xa xỉ", "Nhôm nguyên khối phay xước, Da cừu tự nhiên, Da bò cao cấp"),
                    ("Driver Âm Thanh", "Củ loa", "Custom 40mm Titanium Driver với nam châm Neodymium"),
                    ("Thời Lượng Pin", "Sử dụng", "38 giờ nghe nhạc liên tục ở mức âm lượng tiêu chuẩn"),
                    ("Hộp Phụ Kiện", "Travel Case", "Hộp đựng bằng nhôm aluminum nguyên khối có khóa")
                ]
            },

            # --- SMARTWATCHES & WEARABLES ---
            {
                "title": "Apple Watch Ultra 2 (Khung Titanium Tự Nhiên 49mm, Dây Ocean Xanh Đậm)",
                "slug": "apple-watch-ultra-2-titanium-49mm-ocean",
                "sku": "APL-AWU2-49-OCEAN",
                "brand_slug": "apple",
                "category_slug": "smartwatches",
                "price": 21490000,
                "original_price": 22990000,
                "discount_percent": 6,
                "thumbnail": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&auto=format&fit=crop&q=80",
                "gallery": [
                    "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&auto=format&fit=crop&q=80"
                ],
                "brief_desc": "Vỏ Titanium 49mm cấp hàng không vũ trụ, Màn hình kính sapphire độ sáng 3000 nits, Chip SiP S9 hỗ trợ cử chỉ Chạm hai lần (Double Tap), GPS tần số kép L1 & L5 cực kỳ chính xác.",
                "full_desc": "Chiếc đồng hồ thể thao chuyên nghiệp bền bỉ nhất cho vận động viên marathon, lặn biển sâu 40m và thám hiểm địa hình khắc nghiệt. Thời lượng pin 72 giờ ở chế độ tiết kiệm năng lượng.",
                "stock": 20,
                "rating": 4.97,
                "review_count": 160,
                "is_featured": True,
                "badge": "TITANIUM 49MM 3000NITS",
                "specs": [
                    ("Chất Liệu Vỏ", "Khung viền", "Titanium Cấp 5 hàng không vũ trụ nhô cao bảo vệ mặt kính"),
                    ("Mặt Kính", "Vật liệu", "Tinh thể Sapphire phẳng chống trầy xước cấp độ cao nhất"),
                    ("Độ Bền & Lặn", "Chứng chỉ", "Kháng nước 100m, Chứng nhận EN13319 thiết bị đo độ sâu khi lặn"),
                    ("Định Vị", "Hệ thống GPS", "GPS tần số kép chính xác L1 và L5, còi báo động khẩn cấp 86dB")
                ]
            },
            {
                "title": "Samsung Galaxy Watch Ultra (Titanium 47mm LTE, Dây Marine Xám Đậm)",
                "slug": "samsung-galaxy-watch-ultra-47mm-lte-gray",
                "sku": "SAM-GWU-47-LTE",
                "brand_slug": "samsung",
                "category_slug": "smartwatches",
                "price": 15990000,
                "original_price": 17990000,
                "discount_percent": 11,
                "thumbnail": "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=800&auto=format&fit=crop&q=80",
                "gallery": [
                    "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=800&auto=format&fit=crop&q=80"
                ],
                "brief_desc": "Thiết kế đệm Cushion sáng tạo, Khung viền Titanium cấp 4 chịu nhiệt độ từ -20°C đến 55°C, Nút Quick Button vật lý tùy biến hành động, Tính năng theo dõi chỉ số lão hóa sinh học BioActive.",
                "full_desc": "Đồng hồ thông minh Android cao cấp nhất với vi xử lý 3nm đầu tiên trên thiết bị đeo. Phân tích chỉ số năng lượng cơ thể Energy Score và cảnh báo nguy cơ ngưng thở khi ngủ được FDA chứng nhận.",
                "stock": 15,
                "rating": 4.9,
                "review_count": 82,
                "is_featured": False,
                "badge": "CHÍNH XÁC Y TẾ",
                "specs": [
                    ("Bộ Xử Lý", "Tiến trình", "Exynos W1000 3nm 5 nhân siêu tiết kiệm pin"),
                    ("Khung Vỏ", "Titanium Grade 4", "Độ bền chuẩn quân đội MIL-STD-810H và chống nước 10 ATM"),
                    ("Màn Hình", "Sapphire Glass", "1.5 inch Super AMOLED 3000 nits, Always On Display"),
                    ("Cảm Biến", "BioActive Sensor", "Điện tâm đồ ECG, Huyết áp, Thành phần cơ thể BIA, SpO2")
                ]
            },

            # --- MONITORS & DISPLAYS ---
            {
                "title": "Apple Studio Display 27\" 5K Retina (Mặt Kính Cấu Trúc Nano, Chân Đế Chỉnh Độ Nghiêng)",
                "slug": "apple-studio-display-27-5k-nano-texture",
                "sku": "APL-STD-27-5K-NANO",
                "brand_slug": "apple",
                "category_slug": "monitors",
                "price": 49990000,
                "original_price": 53990000,
                "discount_percent": 7,
                "thumbnail": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=800&auto=format&fit=crop&q=80",
                "gallery": [
                    "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=800&auto=format&fit=crop&q=80"
                ],
                "brief_desc": "Màn hình 27 inch 5K Retina (5120 x 2880), Kính tán xạ Nano-texture chống lóa vượt trội, Chip A13 Bionic điều khiển Camera 12MP Center Stage và dàn 6 loa chuẩn rạp hát.",
                "full_desc": "Màn hình tiêu chuẩn công nghiệp đồ họa và thiết kế sáng tạo. Khung nhôm nguyên khối tối giản tuyệt mỹ, tích hợp 1 cổng Thunderbolt 3 sạc ngược 96W cho Mac và 3 cổng USB-C 10Gbps.",
                "stock": 8,
                "rating": 4.99,
                "review_count": 52,
                "is_featured": True,
                "badge": "5K RETINA NANO-TEXTURE",
                "specs": [
                    ("Độ Phân Giải", "Chi tiết điểm ảnh", "5K (5120 x 2880) tại 218 ppi, 14.7 triệu điểm ảnh"),
                    ("Độ Sáng & Màu Sắc", "Hiển thị màu", "600 nits, Dải màu rộng DCI-P3 1 tỷ màu, True Tone"),
                    ("Mặt Kính", "Xử lý bề mặt", "Mặt kính cấu trúc Nano tán xạ ánh sáng không làm suy giảm tương phản"),
                    ("Tích Hợp", "Camera & Loa", "Camera 12MP Ultra-Wide Center Stage, 6 loa âm thanh vòm Spatial Audio")
                ]
            },
            {
                "title": "Dell UltraSharp 32\" 6K Monitor (U3224KB, IPS Black 6144x3456, 4K HDR Webcam)",
                "slug": "dell-ultrasharp-32-6k-u3224kb",
                "sku": "DEL-U3224KB-6K",
                "brand_slug": "dell",
                "category_slug": "monitors",
                "price": 64990000,
                "original_price": 69990000,
                "discount_percent": 7,
                "thumbnail": "https://images.unsplash.com/photo-1547119957-637f8679db1e?w=800&auto=format&fit=crop&q=80",
                "gallery": [
                    "https://images.unsplash.com/photo-1547119957-637f8679db1e?w=800&auto=format&fit=crop&q=80"
                ],
                "brief_desc": "Màn hình 6K đầu tiên trên thế giới tích hợp công nghệ IPS Black với tỷ lệ tương phản 2000:1, Cổng Thunderbolt 4 cấp nguồn 140W EPR, Webcam kép 4K HDR HDR thông minh.",
                "full_desc": "Lựa chọn hàng đầu cho trạm làm việc của lập trình viên cao cấp và kiến trúc sư đồ họa 3D. Mật độ điểm ảnh siêu mịn giúp văn bản và đường nét sắc sảo như trang in ấn phẩm cao cấp.",
                "stock": 7,
                "rating": 4.96,
                "review_count": 34,
                "is_featured": False,
                "badge": "6K IPS BLACK 140W EPR",
                "specs": [
                    ("Độ Phân Giải", "Tấm nền", "31.5 inch 6K (6144 x 3456) IPS Black Technology"),
                    ("Tương Phản", "Độ tương phản thực", "2000:1 (Màu đen sâu hơn 41% so với IPS truyền thống)"),
                    ("Màu Sắc", "Độ phủ màu", "99% DCI-P3, 100% sRGB, Delta E < 1.5 cân màu từ nhà máy"),
                    ("Kết Nối Đa Năng", "Thunderbolt 4 Hub", "Thunderbolt 4 (140W), Mini-DP 2.1, HDMI 2.1, Cổng mạng 2.5GbE RJ45")
                ]
            },
            {
                "title": "LG UltraGear 32\" 4K Dual-Mode OLED Gaming Monitor (32GS95UE, 4K 240Hz / FHD 480Hz)",
                "slug": "lg-ultragear-32gs95ue-4k-oled-dual-mode",
                "sku": "LG-32GS95UE-OLED",
                "brand_slug": "asus",
                "category_slug": "monitors",
                "price": 34990000,
                "original_price": 38990000,
                "discount_percent": 10,
                "thumbnail": "https://images.unsplash.com/photo-1593305841991-05c297ba4575?w=800&auto=format&fit=crop&q=80",
                "gallery": [
                    "https://images.unsplash.com/photo-1593305841991-05c297ba4575?w=800&auto=format&fit=crop&q=80"
                ],
                "brief_desc": "Tấm nền WOLED chuẩn điện ảnh, Tính năng Dual-Hz đột phá chuyển đổi tức thì giữa 4K 240Hz đồ họa sắc nét và FHD 480Hz thi đấu Esports đỉnh cao, Thời gian đáp ứng 0.03ms GtG.",
                "full_desc": "Công nghệ âm thanh phát trực tiếp từ bề mặt màn hình Pixel Sound độc quyền mang lại cảm giác âm thanh chuẩn xác theo vị trí chuyển động của vật thể trong khung hình.",
                "stock": 9,
                "rating": 4.97,
                "review_count": 46,
                "is_featured": False,
                "badge": "DUAL-MODE 4K 240HZ / FHD 480HZ",
                "specs": [
                    ("Tấm Nền", "OLED Gaming", "31.5\" 4K UHD (3840 x 2160) Anti-Glare Low Reflection"),
                    ("Tần Số Quét", "Chế độ kép", "Chế độ 1: 4K 240Hz | Chế độ 2: Full HD 480Hz"),
                    ("Tốc Độ", "Response Time", "0.03ms (GtG) siêu tốc loại bỏ hoàn toàn bóng mờ"),
                    ("Tương Thích", "Đồng bộ khung hình", "NVIDIA G-Sync Compatible, AMD FreeSync Premium Pro")
                ]
            },

            # --- PC & AI HARDWARE ---
            {
                "title": "NVIDIA GeForce RTX 5090 Founders Edition 32GB GDDR7",
                "slug": "nvidia-geforce-rtx-5090-founders-edition-32gb",
                "sku": "NV-RTX5090-32G-FE",
                "brand_slug": "nvidia",
                "category_slug": "pc-components",
                "price": 59990000,
                "original_price": 64990000,
                "discount_percent": 8,
                "thumbnail": "https://images.unsplash.com/photo-1587202372775-e229f172b9d7?w=800&auto=format&fit=crop&q=80",
                "gallery": [
                    "https://images.unsplash.com/photo-1587202372775-e229f172b9d7?w=800&auto=format&fit=crop&q=80",
                    "https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=800&auto=format&fit=crop&q=80"
                ],
                "brief_desc": "Kiến trúc Blackwell B200 tối thượng, 32GB GDDR7 bus 512-bit băng thông 1.8 TB/s, 21,760 nhân CUDA, 3,300 AI TOPS huấn luyện LLM và Gaming Full Path Tracing.",
                "full_desc": "NVIDIA GeForce RTX 5090 là đỉnh cao điện toán cá nhân thế giới. Với dung lượng VRAM khổng lồ 32GB GDDR7 thế hệ mới, chạy mô hình ngôn ngữ LLaMA 70B và Flux AI nội bộ với tốc độ suy luận thời gian thực.",
                "stock": 8,
                "rating": 5.0,
                "review_count": 92,
                "is_featured": True,
                "badge": "BLACKWELL 3,300 TOPS",
                "specs": [
                    ("Kiến Trúc", "Vi kiến trúc", "NVIDIA Blackwell (TSMC 4NP)"),
                    ("Thông Số Nhân", "Nhân CUDA", "21,760 Cores"),
                    ("Bộ Nhớ Đồ Họa", "VRAM & Bus", "32GB GDDR7 512-bit (Băng thông 1,792 GB/s)"),
                    ("Trí Tuệ Nhân Tạo", "Hiệu năng AI", "3,300 Tensor TOPS (DLSS 4 Multi-Frame)"),
                    ("Điện Năng & Cổng", "Công suất TDP", "600W (Nguồn khuyến nghị 1000W-1200W)")
                ]
            },
            {
                "title": "NVIDIA GeForce RTX 4090 Founders Edition 24GB GDDR6X",
                "slug": "nvidia-geforce-rtx-4090-fe-24gb",
                "sku": "NV-RTX4090-24G-FE",
                "brand_slug": "nvidia",
                "category_slug": "pc-components",
                "price": 49990000,
                "original_price": 54990000,
                "discount_percent": 9,
                "thumbnail": "https://images.unsplash.com/photo-1591488320449-011701bb6704?w=800&auto=format&fit=crop&q=80",
                "gallery": [
                    "https://images.unsplash.com/photo-1591488320449-011701bb6704?w=800&auto=format&fit=crop&q=80"
                ],
                "brief_desc": "Kiến trúc Ada Lovelace, 24GB GDDR6X, 16,384 nhân CUDA, 1,321 AI TOPS, Công nghệ DLSS 3.5 Frame Generation và bộ mã hóa kép Dual NVENC AV1.",
                "full_desc": "Biểu tượng huyền thoại về card đồ họa hiệu năng cao. Lựa chọn số 1 của các nhà nghiên cứu thị giác máy tính và các studio render VFX 3D trên toàn cầu.",
                "stock": 14,
                "rating": 4.98,
                "review_count": 210,
                "is_featured": True,
                "badge": "CHUẨN STUDIO ĐỒ HỌA",
                "specs": [
                    ("Kiến Trúc", "Vi kiến trúc", "NVIDIA Ada Lovelace"),
                    ("Thông Số Nhân", "Nhân CUDA", "16,384 Cores"),
                    ("Bộ Nhớ Đồ Họa", "VRAM", "24GB GDDR6X 384-bit"),
                    ("Trí Tuệ Nhân Tạo", "Tensor Cores", "4th Gen Tensor Cores (1,321 AI TOPS)"),
                    ("Mã Hóa Video", "NVENC", "Bộ mã hóa kép 8th Gen NVENC hỗ trợ AV1")
                ]
            },
            {
                "title": "NVIDIA Jetson AGX Orin Developer Kit 64GB (275 TOPS AI Edge)",
                "slug": "nvidia-jetson-agx-orin-developer-kit-64gb",
                "sku": "NV-JETSON-AGX-64G",
                "brand_slug": "nvidia",
                "category_slug": "pc-components",
                "price": 52990000,
                "original_price": 56000000,
                "discount_percent": 5,
                "thumbnail": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=800&auto=format&fit=crop&q=80",
                "gallery": [
                    "https://images.unsplash.com/photo-1518770660439-4636190af475?w=800&auto=format&fit=crop&q=80"
                ],
                "brief_desc": "Máy tính nhúng AI mạnh nhất thế giới với 275 TOPS, 64GB LPDDR5, 2048 nhân GPU Ampere + 64 Tensor Cores, hỗ trợ ROS2 & Isaac Sim.",
                "full_desc": "Jetson AGX Orin mang lại bước nhảy vọt gấp 8 lần về hiệu năng. Thiết kế chuyên biệt cho xe tự hành, cánh tay robot công nghiệp và phân tích luồng video nhiều kênh chuẩn AI Edge.",
                "stock": 8,
                "rating": 4.96,
                "review_count": 38,
                "is_featured": False,
                "badge": "ROBOTICS 275 TOPS",
                "specs": [
                    ("Năng Lực AI", "Hiệu năng tính toán", "275 TOPS (INT8)"),
                    ("GPU", "Kiến trúc GPU", "2,048-core Ampere với 64 Tensor Cores"),
                    ("Bộ Nhớ Hệ Thống", "RAM", "64GB 256-bit LPDDR5 (204.8 GB/s)"),
                    ("Công Suất", "Tùy biến điện áp", "15W - 60W")
                ]
            },

            # --- GAMING & CONSOLES ---
            {
                "title": "Sony PlayStation 5 Pro 2TB (PlayStation Spectral Super Resolution PSSR)",
                "slug": "sony-playstation-5-pro-2tb",
                "sku": "SNY-PS5PRO-2TB",
                "brand_slug": "sony",
                "category_slug": "consoles",
                "price": 22990000,
                "original_price": 24990000,
                "discount_percent": 8,
                "thumbnail": "https://images.unsplash.com/photo-1606813907291-d86efa9b94db?w=800&auto=format&fit=crop&q=80",
                "gallery": [
                    "https://images.unsplash.com/photo-1606813907291-d86efa9b94db?w=800&auto=format&fit=crop&q=80"
                ],
                "brief_desc": "GPU nâng cấp thêm 67% đơn vị tính toán Compute Units, Ray Tracing nâng cao gấp 3 lần, Công nghệ nâng cấp hình ảnh bằng học máy PSSR 4K 60FPS ổn định tuyệt đối, Ổ cứng SSD 2TB.",
                "full_desc": "Cỗ máy chơi game mạnh nhất lịch sử thương hiệu PlayStation. Tay cầm DualSense với tính năng Haptic Feedback và Adaptive Triggers cho trải nghiệm nhập vai chân thực đến từng rung động.",
                "stock": 25,
                "rating": 4.98,
                "review_count": 180,
                "is_featured": True,
                "badge": "PS5 PRO 4K 60FPS",
                "specs": [
                    ("Xử Lý Đồ Họa", "GPU Architecture", "RDNA nâng cấp với Ray Tracing thế hệ mới (16.7 TFLOPS)"),
                    ("Lưu Trữ", "Ổ cứng siêu tốc", "2TB NVMe SSD chuẩn PCIe Gen 4 (5.5 GB/s Raw)"),
                    ("Công Nghệ AI", "Upscaling", "PlayStation Spectral Super Resolution (PSSR AI)"),
                    ("Kết Nối", "Chuẩn mạng", "Wi-Fi 7 thế hệ mới, HDMI 2.1 4K 120Hz / 8K VRR")
                ]
            },
            {
                "title": "Nintendo Switch – OLED Model (Mario Red Edition, Màn Hình 7.0\" OLED Rực Rỡ)",
                "slug": "nintendo-switch-oled-mario-red",
                "sku": "NTD-SWOLED-MRED",
                "brand_slug": "nintendo",
                "category_slug": "consoles",
                "price": 7990000,
                "original_price": 8690000,
                "discount_percent": 8,
                "thumbnail": "https://images.unsplash.com/photo-1578303512597-8be936742317?w=800&auto=format&fit=crop&q=80",
                "gallery": [
                    "https://images.unsplash.com/photo-1578303512597-8be936742317?w=800&auto=format&fit=crop&q=80"
                ],
                "brief_desc": "Phiên bản giới hạn đỏ đặc trưng Mario, Màn hình 7 inch OLED tương phản sâu tuyệt đối, Chân đế bản rộng có thể điều chỉnh nhiều góc độ, Cổng LAN có dây trên dock sạc.",
                "full_desc": "Mang cả thế giới game Nintendo đỉnh cao theo bạn tới mọi nơi. Chơi mượt mà các siêu phẩm huyền thoại The Legend of Zelda: Tears of the Kingdom, Super Mario Bros. Wonder.",
                "stock": 30,
                "rating": 4.95,
                "review_count": 210,
                "is_featured": False,
                "badge": "MARIO LIMITED EDITION",
                "specs": [
                    ("Màn Hình", "Tấm nền hiển thị", "7.0 inch OLED cảm ứng điện dung đa điểm (1280 x 720)"),
                    ("Chế Độ Chơi", "Đa dạng 3 phong cách", "TV Mode, Tabletop Mode, Handheld Mode"),
                    ("Lưu Trữ", "Bộ nhớ trong", "64GB bộ nhớ (hỗ trợ mở rộng thẻ nhớ MicroSD 2TB)"),
                    ("Thời Lượng Pin", "Sử dụng", "Từ 4.5 đến 9 giờ tùy theo độ nặng của trò chơi")
                ]
            },

            # --- HIGH-END ACCESSORIES ---
            {
                "title": "Cáp Bọc Dù Apple Thunderbolt 5 Pro (2m, Tốc Độ 80Gbps - 120Gbps, Sạc 240W)",
                "slug": "apple-thunderbolt-5-pro-cable-2m",
                "sku": "APL-TB5-2M-PRO",
                "brand_slug": "apple",
                "category_slug": "accessories",
                "price": 3190000,
                "original_price": 3590000,
                "discount_percent": 11,
                "thumbnail": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=800&auto=format&fit=crop&q=80",
                "gallery": [
                    "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=800&auto=format&fit=crop&q=80"
                ],
                "brief_desc": "Dây bọc sợi bện màu đen không rối, Băng thông dữ liệu 80Gbps và Bandwidth Boost 120Gbps, Xuất cùng lúc nhiều màn hình 8K 60Hz, Hỗ trợ sạc công suất khủng 240W EPR.",
                "full_desc": "Cáp kết nối tối thượng giữa MacBook Pro M4, iPhone 16 Pro và các hệ thống lưu trữ RAID hoặc máy trạm GPU chuyên nghiệp. Khả năng tương thích ngược trọn vẹn với Thunderbolt 4, Thunderbolt 3 và USB4.",
                "stock": 45,
                "rating": 4.98,
                "review_count": 89,
                "is_featured": False,
                "badge": "THUNDERBOLT 5 120GBPS",
                "specs": [
                    ("Băng Thông", "Tốc độ truyền dữ liệu", "80 Gbps hai chiều (Tăng tốc tối đa 120 Gbps)"),
                    ("Công Suất Sạc", "Power Delivery", "Lên đến 240W EPR sạc nhanh cho mọi dòng máy"),
                    ("Xuất Hình", "Độ phân giải video", "Hỗ trợ chuẩn DisplayPort 2.1 xuất 8K 60Hz hoặc 4K 240Hz")
                ]
            },
            {
                "title": "Bàn Phím Cơ Keychron Q1 Max (Full Nhôm CNC, 3 Chế Độ Kết Nối, Gateron Jupiter Brown)",
                "slug": "keychron-q1-max-full-aluminum-wireless",
                "sku": "KCH-Q1MAX-ALU",
                "brand_slug": "logitech-keychron",
                "category_slug": "accessories",
                "price": 4890000,
                "original_price": 5490000,
                "discount_percent": 10,
                "thumbnail": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800&auto=format&fit=crop&q=80",
                "gallery": [
                    "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800&auto=format&fit=crop&q=80"
                ],
                "brief_desc": "Thân vỏ nhôm nguyên khối 6063 cắt CNC chuẩn xác, Cấu trúc Double-Gasket êm ái triệt tiêu tạp âm, Kết nối không dây 2.4GHz độ trễ 1000Hz, Bluetooth 5.1 và có dây Type-C.",
                "full_desc": "Chiếc bàn phím cơ hoàn thiện đỉnh cao dành cho giới coder và kỹ sư công nghệ. Tương thích hoàn hảo chuyển đổi giữa phím bấm macOS và Windows chỉ với một gạt công tắc.",
                "stock": 22,
                "rating": 4.96,
                "review_count": 110,
                "is_featured": False,
                "badge": "NHÔM CNC CAO CẤP",
                "specs": [
                    ("Khung Vỏ", "Vật liệu", "Nhôm nguyên khối 6063 xử lý bề mặt anodized cao cấp"),
                    ("Cấu Trúc", "Đệm phím", "Double-Gasket Design kết hợp 5 lớp foam tiêu âm IXPE & PET"),
                    ("Switch", "Công tắc phím", "Gateron Jupiter Brown bôi trơn sẵn từ nhà máy"),
                    ("Tương Thích", "Hệ điều hành", "Hỗ trợ QMK/VIA tùy biến toàn bộ phím cho Mac & Windows")
                ]
            },
            {
                "title": "Chuột Không Dây Logitech MX Master 3S (Cảm Biến Darkfield 8K DPI, Cuộn Magspeed)",
                "slug": "logitech-mx-master-3s-wireless-mouse",
                "sku": "LOG-MXM3S-GRY",
                "brand_slug": "logitech-keychron",
                "category_slug": "accessories",
                "price": 2490000,
                "original_price": 2890000,
                "discount_percent": 13,
                "thumbnail": "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=800&auto=format&fit=crop&q=80",
                "gallery": [
                    "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=800&auto=format&fit=crop&q=80"
                ],
                "brief_desc": "Cảm biến quang học 8000 DPI di chuyển mượt mà ngay trên mặt kính trong suốt, Công nghệ Quiet Clicks giảm 90% tiếng ồn bấm chuột, Con lăn điện từ MagSpeed cuộn 1000 dòng/giây.",
                "full_desc": "Chuột công thái học tiêu chuẩn vàng cho nhà thiết kế và lập trình viên. Hỗ trợ tính năng Logitech Flow luân chuyển con trỏ và copy paste dữ liệu mượt mà giữa máy tính Mac và Windows.",
                "stock": 50,
                "rating": 4.97,
                "review_count": 320,
                "is_featured": False,
                "badge": "CUỘN TỪ TRƯỜNG 1000 DÒNG/S",
                "specs": [
                    ("Cảm Biến", "Độ nhạy", "Darkfield High Precision 200 - 8000 DPI (chạy được trên kính)"),
                    ("Con Lăn", "Cơ chế cuộn", "MagSpeed Electromagnetic Scrolling siêu mượt và chuẩn xác"),
                    ("Thời Lượng Pin", "Sạc nhanh", "Pin dùng 70 ngày sau một lần sạc đầy (1 phút sạc dùng 3 giờ)")
                ]
            },

            # --- SYNERGY COMBO BUNDLES ---
            {
                "title": "Titan Combo: The Neural Creator Rig (iPhone 16 Pro Max 1TB + RTX 5090 32GB)",
                "slug": "combo-neural-creator-rig-ip16pm-rtx5090",
                "sku": "CMB-NEURAL-01",
                "brand_slug": "titan-synergy",
                "category_slug": "bundles",
                "price": 98990000,
                "original_price": 111980000,
                "discount_percent": 12,
                "thumbnail": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=800&auto=format&fit=crop&q=80",
                "gallery": [
                    "https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=800&auto=format&fit=crop&q=80"
                ],
                "brief_desc": "Bộ giải pháp tối thượng: iPhone 16 Pro Max 1TB Titan quay 4K120fps ProRes kết hợp Siêu card đồ họa NVIDIA RTX 5090 32GB GDDR7. Tặng kèm Cáp Thunderbolt 5 Pro và Bản quyền DaVinci Studio.",
                "full_desc": "The Neural Creator Rig là gói phần cứng trong mơ dành cho các đạo diễn công nghệ và nhà nghiên cứu Generative AI. Quay phim chuẩn Apple Log, truyền tải tức thì sang máy trạm RTX 5090 để chạy AI Upscaling và Render với tốc độ chưa từng có. Tiết kiệm ngay gần 13 triệu VNĐ.",
                "stock": 6,
                "rating": 5.0,
                "review_count": 31,
                "is_featured": True,
                "badge": "TIẾT KIỆM 12.990.000₫",
                "specs": [
                    ("Thành Phần Di Động", "Điện thoại Flagship", "iPhone 16 Pro Max 1TB Desert Titanium"),
                    ("Thành Phần Điện Toán", "Siêu GPU AI", "NVIDIA GeForce RTX 5090 32GB GDDR7"),
                    ("Quà Tặng Kèm", "Phụ kiện cao cấp", "Cáp Apple Thunderbolt 5 Pro 2m (Trị giá 3.190.000₫) + Bản quyền Studio"),
                    ("Bảo Hành", "Cam kết dịch vụ", "Bảo hành 24 tháng chính hãng, 1 đổi 1 tận nơi trong 30 ngày")
                ]
            },
            {
                "title": "Titan Combo: Edge AI & Mobile Vision Lab (iPhone 16 Pro 256GB + Jetson AGX Orin 64GB)",
                "slug": "combo-edge-ai-vision-lab",
                "sku": "CMB-EDGEVISION-02",
                "brand_slug": "titan-synergy",
                "category_slug": "bundles",
                "price": 79990000,
                "original_price": 89980000,
                "discount_percent": 11,
                "thumbnail": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=800&auto=format&fit=crop&q=80",
                "gallery": [
                    "https://images.unsplash.com/photo-1518770660439-4636190af475?w=800&auto=format&fit=crop&q=80"
                ],
                "brief_desc": "Phòng lab thu nhỏ cho kỹ sư AI: iPhone 16 Pro quét đám mây điểm 3D LiDAR Scanner + NVIDIA Jetson AGX Orin 64GB 275 TOPS xử lý SLAM & Robot tự hành.",
                "full_desc": "Giải pháp toàn diện đưa nghiên cứu thị giác máy tính từ lý thuyết vào thực tế. Khai thác dữ liệu cảm biến đa tầng từ iPhone và sức mạnh xử lý nhúng số 1 của NVIDIA.",
                "stock": 5,
                "rating": 4.95,
                "review_count": 19,
                "is_featured": False,
                "badge": "TIẾT KIỆM 9.990.000₫",
                "specs": [
                    ("Thu Thập Dữ Liệu", "Thiết bị cảm biến", "iPhone 16 Pro 256GB (LiDAR + 48MP Macro)"),
                    ("Bộ Xử Lý Biên", "Edge Computing", "NVIDIA Jetson AGX Orin 64GB (275 TOPS)"),
                    ("Phần Mềm Hỗ Trợ", "Frameworks", "Tích hợp sẵn ROS2 Humble, PyTorch, Isaac SDK, CoreML")
                ]
            }
        ]

        created_products = []
        for p_item in products_list:
            b_obj = brand_map.get(p_item["brand_slug"])
            c_obj = category_map.get(p_item["category_slug"])

            p = Product(
                id=str(uuid.uuid4()),
                title=p_item["title"],
                slug=p_item["slug"],
                sku=p_item["sku"],
                brand_id=b_obj.id if b_obj else None,
                category_id=c_obj.id if c_obj else None,
                price=p_item["price"],
                original_price=p_item["original_price"],
                discount_percent=p_item["discount_percent"],
                thumbnail=p_item["thumbnail"],
                gallery=p_item.get("gallery", [p_item["thumbnail"]]),
                brief_desc=p_item["brief_desc"],
                full_desc=p_item["full_desc"],
                stock=p_item["stock"],
                rating=p_item["rating"],
                review_count=p_item["review_count"],
                is_featured=p_item["is_featured"],
                is_bundle=(p_item["category_slug"] == "bundles"),
                badge=p_item["badge"],
                created_at=datetime.utcnow()
            )
            db.add(p)
            db.flush()

            # Thông số kỹ thuật
            for idx, spec in enumerate(p_item.get("specs", [])):
                s = ProductSpecification(
                    id=str(uuid.uuid4()),
                    product_id=p.id,
                    spec_group=spec[0],
                    spec_key=spec[1],
                    spec_value=spec[2],
                    order_index=idx
                )
                db.add(s)

            # Đánh giá mẫu xác thực
            r1 = Review(
                id=str(uuid.uuid4()),
                product_id=p.id,
                author_name="Nguyễn Hoàng Nam (Tech Lead)",
                rating=5,
                comment="Sản phẩm nguyên seal chính hãng, đầy đủ hóa đơn VAT. Giao hàng hỏa tốc trong 2 giờ tại TP.HCM, đóng gói cẩn thận 3 lớp chống sốc.",
                verified_purchase=True
            )
            r2 = Review(
                id=str(uuid.uuid4()),
                product_id=p.id,
                author_name="Trần Thảo Ly (Senior Designer)",
                rating=5,
                comment="Dịch vụ hỗ trợ khách hàng rất chuyên nghiệp, thiết kế tinh tế và trải nghiệm sử dụng hoàn toàn xứng đáng với mức giá cao cấp.",
                verified_purchase=True
            )
            db.add_all([r1, r2])
            created_products.append(p)

        db.commit()
        print(f"✅ Đã tạo thành công {len(created_products)} sản phẩm điện tử cao cấp thuộc {len(categories_data)} danh mục!")

    except Exception as e:
        db.rollback()
        print(f"❌ Lỗi khi nạp dữ liệu: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed()
