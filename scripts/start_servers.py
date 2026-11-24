import os
import sys
import subprocess
import time

os.environ["DISABLE_SQLALCHEMY_CEXT"] = "1"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API_DIR = os.path.join(BASE_DIR, "apps", "api")
WEB_DIR = os.path.join(BASE_DIR, "apps", "web")

venv_python = os.path.join(BASE_DIR, ".venv", "Scripts", "python.exe")
if not os.path.exists(venv_python):
    venv_python = os.path.join(BASE_DIR, ".venv", "bin", "python")

python_bin = venv_python if os.path.exists(venv_python) else sys.executable

print(f"🌟 [TECH STORE] Using Python: {python_bin}")
print("🌟 [TECH STORE] Starting FastAPI Backend on http://127.0.0.1:8000...")
api_proc = subprocess.Popen(
    [python_bin, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"],
    cwd=API_DIR
)

print("🌟 [TECH STORE] Starting Next.js Web Server on http://localhost:3000...")
web_proc = subprocess.Popen(
    "npm run dev",
    shell=True,
    cwd=WEB_DIR
)

print("")
print("==========================================================================")
print("🚀 TECH STORE JAPAN IS RUNNING!")
print("   - Frontend URL:        http://localhost:3000")
print("   - Backend Swagger API: http://localhost:8000/docs")
print("   - Health check:        http://localhost:8000/health")
print("==========================================================================")
print("")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nStopping servers...")
    api_proc.terminate()
    if sys.platform == "win32":
        subprocess.run(f"taskkill /F /T /PID {web_proc.pid}", shell=True, capture_output=True)
    else:
        web_proc.terminate()
