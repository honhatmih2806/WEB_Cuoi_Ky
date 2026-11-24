@echo off
setlocal
chcp 65001 >nul
title UteTechStore — Server Launcher
color 0B

set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

set DISABLE_SQLALCHEMY_CEXT=1

if exist "%SCRIPT_DIR%.venv\Scripts\python.exe" (
    set "PY_CMD=%SCRIPT_DIR%.venv\Scripts\python.exe"
) else (
    set "PY_CMD=python"
)

echo ==============================================================================
echo       UteTechStore (UTE TECH STORE) - PREMIUM ELECTRONICS STORE
echo ==============================================================================
echo.
echo [Khoi dong] Dang kich hoat Backend (:8000) va Frontend (:3000)...
echo.

start http://localhost:3000
"%PY_CMD%" "%SCRIPT_DIR%scripts\start_servers.py"
