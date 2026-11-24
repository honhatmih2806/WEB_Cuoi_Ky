# UteTechStore - PowerShell Launcher
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$env:DISABLE_SQLALCHEMY_CEXT = "1"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
if (-not $ScriptDir) { $ScriptDir = Get-Location }
Set-Location $ScriptDir

$PyCmd = if (Test-Path "$ScriptDir\.venv\Scripts\python.exe") {
    "$ScriptDir\.venv\Scripts\python.exe"
} else {
    "python"
}

Write-Host "==============================================================================" -ForegroundColor Cyan
Write-Host "       UteTechStore (UTE TECH STORE) - KHỞI ĐỘNG HỆ THỐNG" -ForegroundColor Cyan
Write-Host "==============================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "[Khởi động] Đang kích hoạt Backend (:8000) và Frontend (:3000)..." -ForegroundColor Yellow
Write-Host ""

Start-Process "http://localhost:3000"
& $PyCmd "$ScriptDir\scripts\start_servers.py"
