@echo off
REM Script principal raiz - doble clic para ejecutar todo sin admin
setlocal
cd /d %~dp0
echo === Investigacion C2-DECT Lite - Raiz ===
where py >nul 2>nul
if %errorlevel%==0 (
  py ejecutar.py
) else (
  python ejecutar.py
)
pause
