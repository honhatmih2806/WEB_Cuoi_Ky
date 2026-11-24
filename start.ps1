# UteTechStore - PowerShell Launcher
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$env:DISABLE_SQLALCHEMY_CEXT = "1"

Write-Host "==============================================================================" -ForegroundColor Cyan
Write-Host "       UteTechStore (UTE TECH STORE) - KHỞI ĐỘNG HỆ THỐNG" -ForegroundColor Cyan
Write-Host "==============================================================================" -ForegroundColor Cyan
Write-Host ""

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
if (-not $ScriptDir) { $ScriptDir = Get-Location }
Set-Location $ScriptDir

# 1. Check Python
$PyCmd = if (Test-Path "$ScriptDir\.venv\Scripts\python.exe") {
    "$ScriptDir\.venv\Scripts\python.exe"
} else {
    "python"
}
Write-Host "[OK] Sử dụng Python: $PyCmd" -ForegroundColor Green

# 2. Check Node / npm
if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
    Write-Host "[CẢNH BÁO] Không tìm thấy Node.js / npm trong PATH! Vui lòng cài đặt Node.js." -ForegroundColor Red
}

# 3. Launch Backend FastAPI
Write-Host "[1/2] Đang khởi động Backend FastAPI tại http://127.0.0.1:8000 ..." -ForegroundColor Yellow
Start-Process -FilePath "cmd.exe" -ArgumentList "/k cd /d `"$ScriptDir\apps\api`" && set DISABLE_SQLALCHEMY_CEXT=1 && `"$PyCmd`" -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload"

Start-Sleep -Seconds 3

# 4. Launch Frontend Next.js
Write-Host "[2/2] Đang khởi động Frontend Next.js tại http://localhost:3000 ..." -ForegroundColor Yellow
Start-Process -FilePath "cmd.exe" -ArgumentList "/k cd /d `"$ScriptDir\apps\web`" && npm run dev"

Start-Sleep -Seconds 4

Write-Host ""
Write-Host "==============================================================================" -ForegroundColor Green
Write-Host "✅ [THÀNH CÔNG] Toàn bộ hệ thống UteTechStore đã khởi chạy!" -ForegroundColor Green
Write-Host "  👉 Cửa hàng Web (Next.js):     http://localhost:3000" -ForegroundColor White
Write-Host "  👉 Tài liệu Swagger API:       http://localhost:8000/docs" -ForegroundColor White
Write-Host "  👉 Kiểm tra sức khỏe hệ thống: http://localhost:8000/health" -ForegroundColor White
Write-Host "==============================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Đang mở trình duyệt đến http://localhost:3000 ..." -ForegroundColor Cyan

Start-Process "http://localhost:3000"
