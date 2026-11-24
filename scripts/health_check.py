import sys
import os
import requests

def check():
    print("🔍 [health_check] Đang kiểm tra trạng thái hệ thống Titan Silicon...")
    
    # 1. API Health Check
    api_url = os.getenv("API_URL", "http://localhost:8000/health")
    try:
        res = requests.get(api_url, timeout=3)
        if res.status_code == 200:
            print("✅ Backend API (FastAPI): HEALTHY (HTTP 200)")
        else:
            print(f"⚠️ Backend API phản hồi mã: {res.status_code}")
    except Exception as e:
        print(f"ℹ️ Backend API chưa mở tại {api_url} (hãy chạy ./dev.sh hoặc ./start.sh)")

    # 2. Web Frontend Check
    web_url = os.getenv("WEB_URL", "http://localhost:3000")
    try:
        res = requests.get(web_url, timeout=3)
        if res.status_code == 200:
            print("✅ Web Frontend (Next.js): HEALTHY (HTTP 200)")
        else:
            print(f"⚠️ Web Frontend phản hồi mã: {res.status_code}")
    except Exception as e:
        print(f"ℹ️ Web Frontend chưa mở tại {web_url}")

if __name__ == "__main__":
    check()
