@echo off
chcp 65001 >nul
title Frontend ULTRATHINK - Sinistros Control

echo.
echo ================================================
echo   🚀 FRONTEND ULTRATHINK - SINISTROS CONTROL
echo ================================================
echo.

echo 📦 Instalando dependências...
cd frontend
call npm install

if %ERRORLEVEL% NEQ 0 (
    echo ❌ Erro ao instalar dependências
    pause
    exit /b 1
)

echo.
echo ✅ Dependências instaladas com sucesso!
echo.
echo 🚀 Iniciando servidor de desenvolvimento...
echo.
echo 🌐 URL: http://localhost:5173
echo 🎯 Dashboard moderno baseado em BR SAMOR
echo 🎨 Design system ULTRATHINK implementado
echo.

start "" "http://localhost:5173"
call npm run dev

pause 