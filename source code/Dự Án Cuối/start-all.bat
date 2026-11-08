@echo off
chcp 65001 > nul
title AI-Native Commerce - Multi-Service Launcher (NET108)

echo ======================================================================
echo    AI-NATIVE COMMERCE - FPT POLYTECHNIC NET108 FINAL PROJECT
echo ======================================================================
echo.
echo [1/3] Đang khởi động Backend C# .NET API (dotnet run trên Cổng 5000)...
start "AI-Native Commerce Backend (C# .NET)" cmd /k "cd /d ""%~dp0backend-dotnet"" && dotnet run"

timeout /t 3 /nobreak > nul

echo [2/3] Đang khởi động AI Microservice (Python FastAPI trên Cổng 8000)...
start "AI-Native Commerce AI Service (Python)" cmd /k "cd /d ""%~dp0ai-service"" && python main.py"

timeout /t 3 /nobreak > nul

echo [3/3] Đang khởi động Frontend Web UI (React Vite trên Cổng 3000)...
start "AI-Native Commerce Frontend (React)" cmd /k "cd /d ""%~dp0frontend"" && npm run dev"

timeout /t 2 /nobreak > nul

echo.
echo [4/4] Đang tự động mở Trình duyệt Web tại http://localhost:3000 ...
start http://localhost:3000

echo.
echo ======================================================================
echo    HỆ THỐNG ĐÃ SẴN SÀNG!
echo ======================================================================
echo  - Frontend Web UI:     http://localhost:3000
echo  - Backend C# .NET API: http://localhost:5000  (Kiểm tra: /health)
echo  - AI Microservice:     http://localhost:8000
echo ======================================================================
echo.
pause
