@echo off
chcp 65001 > nul
title AI-Native Commerce - Multi-Service Launcher

echo ======================================================================
echo    AI-NATIVE COMMERCE - FPT POLYTECHNIC NET108 FINAL PROJECT
echo ======================================================================
echo.
echo [1/3] Đang khởi động Backend API (Port 5000)...
start "AI-Native Commerce Backend (Port 5000)" cmd /k "cd /d %~dp0backend && npm run dev"

timeout /t 3 /nobreak > nul

echo [2/3] Đang khởi động AI Service (Port 8000)...
start "AI-Native Commerce AI Service (Port 8000)" cmd /k "cd /d %~dp0ai-service && python main.py"

timeout /t 3 /nobreak > nul

echo [3/3] Đang khởi động Frontend Web App (Port 3000)...
start "AI-Native Commerce Frontend (Port 3000)" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo ======================================================================
echo    TẤT CẢ CÁC DỊCH VỤ ĐÃ ĐƯỢC KHỞI CHẠY THÀNH CÔNG!
echo ======================================================================
echo  - Frontend Web UI:  http://localhost:3000
echo  - Backend REST API: http://localhost:5000
echo  - AI Microservice:  http://localhost:8000
echo ======================================================================
echo.
pause
