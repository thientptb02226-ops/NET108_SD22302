# AI-Native Commerce - PowerShell Launcher for NET108
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "   AI-NATIVE COMMERCE - FPT POLYTECHNIC NET108 FINAL PROJECT" -ForegroundColor Yellow
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

$baseDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# 1. Start Backend C# .NET
Write-Host "[1/3] Đang khởi động Backend C# .NET API (dotnet run trên Cổng 5000)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$baseDir\backend-dotnet'; dotnet run"

Start-Sleep -Seconds 3

# 2. Start Frontend
Write-Host "[2/3] Đang khởi động Frontend Web UI (npm run dev trên Cổng 3000)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$baseDir\frontend'; npm run dev"

Start-Sleep -Seconds 2

# 3. Open Browser
Write-Host "[3/3] Đang mở trình duyệt truy cập http://localhost:3000 ..." -ForegroundColor Magenta
Start-Process "http://localhost:3000"

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "   HỆ THỐNG ĐÃ KHỞI CHẠY VÀ MỞ TRÌNH DUYỆT THÀNH CÔNG!" -ForegroundColor Yellow
Write-Host "   - Frontend Web UI:     http://localhost:3000" -ForegroundColor White
Write-Host "   - Backend C# .NET API: http://localhost:5000" -ForegroundColor White
Write-Host "======================================================================" -ForegroundColor Cyan
