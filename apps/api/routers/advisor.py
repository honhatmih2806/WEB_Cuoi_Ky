from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from core.envelope import ApiResponse
from models.entities import Product, Brand
from schemas.dtos import AdvisorRequest, AdvisorRecommendationDTO
from routers.products import format_product_list_item

router = APIRouter(prefix="/advisor", tags=["AI Synergy Advisor"])

@router.post("/recommend", response_model=ApiResponse[AdvisorRecommendationDTO])
def recommend_synergy_setup(req: AdvisorRequest, db: Session = Depends(get_db)):
    use_case = req.use_case.upper()
    budget = req.budget_range.upper()

    # Query candidate products
    apple_products = db.query(Product).join(Product.brand).filter(Brand.slug == "apple", Product.is_bundle == False).all()
    nvidia_products = db.query(Product).join(Product.brand).filter(Brand.slug == "nvidia", Product.is_bundle == False).all()
    bundles = db.query(Product).filter(Product.is_bundle == True).all()

    matched_iphone = None
    matched_nvidia = None
    matched_bundle = None
    title = ""
    subtitle = ""
    synergy_reason = ""
    benchmarks = {}

    if use_case in ["DEEP_LEARNING", "AI_RESEARCH_LLM"]:
        title = "Trạm Huấn Luyện AI & Quản Trị Mô Hình Di Động"
        subtitle = "Tối ưu hóa huấn luyện LLM cục bộ, suy luận phân tán & giám sát từ xa"
        
        # Match RTX 5090 or RTX 4090
        matched_nvidia = next((p for p in nvidia_products if "5090" in p.title), None) or next((p for p in nvidia_products if "4090" in p.title), None)
        matched_iphone = next((p for p in apple_products if "Pro Max" in p.title), None) or (apple_products[0] if apple_products else None)
        matched_bundle = next((b for b in bundles if "Neural" in b.title or "AI" in b.title), None)
        
        synergy_reason = (
            "Sự kết hợp giữa 32GB/24GB VRAM kiến trúc NVIDIA Ada/Blackwell cho phép chạy trực tiếp các mô hình Llama-3 70B (Quantized) và Stable Diffusion 3. "
            "iPhone 16 Pro Max với chip A18 Pro và kết nối Wi-Fi 7 cho phép quản trị notebook, điều khiển trạm AI từ xa với độ trễ dưới 2ms."
        )
        benchmarks = {
            "AI_Inference_TOPS": "3,300 TOPS (Blackwell + A18 Neural)",
            "LLM_Token_Per_Sec": "115 tokens/s (Llama-3 8B FP16)",
            "VRAM_Capacity": "24GB - 32GB GDDR7",
            "Target_FPS_Cyberpunk_4K": "144+ FPS (DLSS 3.5 Path Tracing)"
        }

    elif use_case in ["4K_PRORES_CINEMA", "CONTENT_CREATION"]:
        title = "Studio Điện Ảnh Di Động & Hậu Kỳ Đồ Họa 8K"
        subtitle = "Quy trình làm phim chuẩn Academy: Ghi hình Apple Log, Dựng phim DaVinci Studio"
        
        matched_iphone = next((p for p in apple_products if "16 Pro" in p.title), None) or (apple_products[0] if apple_products else None)
        matched_nvidia = next((p for p in nvidia_products if "4090" in p.title or "4080" in p.title), None)
        matched_bundle = next((b for b in bundles if "Studio" in b.title or "Creator" in b.title), None)
        
        synergy_reason = (
            "Quay phim 4K 120fps Dolby Vision ProRes trực tiếp vào SSD qua cổng Type-C Thunderbolt 3 trên iPhone. "
            "Chuyển ngay footage vào Premiere/DaVinci Resolve để GPU NVIDIA giải mã bằng bộ mã hóa kép 8th Gen NVENC với tốc độ render nhanh hơn 3.2 lần."
        )
        benchmarks = {
            "Export_Time_10Min_4K": "1 phút 12 giây (Dual NVENC AV1)",
            "Color_Depth": "10-bit 4:2:2 Apple Log Cinema",
            "Max_Timeline_Streams": "8 luồng 4K ProRes đồng thời không drop frame",
            "ProRes_Transfer_Speed": "10 Gbps qua USB 3"
        }

    elif use_case in ["MOBILE_EDGE_AI", "ROBOTICS"]:
        title = "Phòng Thí Nghiệm Thị Giác Máy Tính & Edge AI"
        subtitle = "Thu thập dữ liệu LiDAR thực tế và triển khai mô hình nén on-device"
        
        matched_iphone = next((p for p in apple_products if "Pro" in p.title), None)
        matched_nvidia = next((p for p in nvidia_products if "Jetson" in p.title), None)
        matched_bundle = next((b for b in bundles if "Edge" in b.title or "Vision" in b.title), None)
        
        synergy_reason = (
            "iPhone sử dụng cảm biến LiDAR Scanner và camera góc rộng 48MP làm thiết bị thu thập đám mây điểm 3D (Point Cloud). "
            "NVIDIA Jetson AGX Orin nhận dữ liệu qua ROS2 để xử lý SLAM và điều khiển robot tự hành thời gian thực."
        )
        benchmarks = {
            "Edge_AI_TOPS": "275 TOPS (Jetson AGX Orin)",
            "LiDAR_Scan_Resolution": "Mật độ 100k điểm/giây",
            "Model_Latency_YOLOv9": "4.2 ms / frame",
            "Power_Consumption": "15W - 60W siêu tiết kiệm"
        }

    else: # GAMING_STREAMING
        title = "Gaming Đỉnh Cao 4K & Trạm Streamer Chuyên Nghiệp"
        subtitle = "Full Path Tracing Max Settings kết hợp Webcam Continuity Studio 4K"
        
        matched_nvidia = next((p for p in nvidia_products if "4080" in p.title or "4090" in p.title), None)
        matched_iphone = next((p for p in apple_products if "16" in p.title), None)
        matched_bundle = next((b for b in bundles if "Streamer" in b.title or "Gamer" in b.title), None)
        
        synergy_reason = (
            "GPU NVIDIA GeForce RTX kích hoạt công nghệ Frame Generation và DLSS 3.5 Ray Reconstruction cho trải nghiệm game mượt mà tuyệt đối. "
            "iPhone biến thành webcam studio 4K chất lượng điện ảnh với Center Stage và Portrait Lighting, không tốn tài nguyên CPU máy chủ."
        )
        benchmarks = {
            "4K_Ultra_Gaming_Average": "120 - 180 FPS",
            "Ray_Tracing_Level": "Full Path Tracing Enabled",
            "Stream_Encoder_Overhead": "< 1% (NVIDIA Broadcast & NVENC)",
            "Facecam_Resolution": "4K 60fps HDR TrueDepth"
        }

    iphone_dto = format_product_list_item(matched_iphone) if matched_iphone else None
    nvidia_dto = format_product_list_item(matched_nvidia) if matched_nvidia else None
    bundle_dto = format_product_list_item(matched_bundle) if matched_bundle else None

    # Calculate bundle savings
    individual_total = (matched_iphone.price if matched_iphone else 0) + (matched_nvidia.price if matched_nvidia else 0)
    bundle_price = matched_bundle.price if matched_bundle else int(individual_total * 0.92)
    savings = max(0, individual_total - bundle_price)

    recommendation = AdvisorRecommendationDTO(
        title=title,
        subtitle=subtitle,
        matched_iphone=iphone_dto,
        matched_nvidia=nvidia_dto,
        synergy_bundle=bundle_dto,
        synergy_reason=synergy_reason,
        benchmark_scores=benchmarks,
        total_savings_vnd=savings
    )

    return ApiResponse.ok(data=recommendation)
