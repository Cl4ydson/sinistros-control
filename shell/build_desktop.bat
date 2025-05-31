@echo off
REM 1. Build frontend
cd ../frontend
npm ci
npm run build

REM 2. Build backend
cd ../
call backend/build_backend.bat

REM 3. Pack Electron app
cd shell
npm ci
npm run pack

REM instalador em dist/*.exe