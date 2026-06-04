@echo off
title Servidor Ginkana Botanica
echo ============================================
echo   SERVIDOR LOCAL - GINKANA BOTANICA
echo ============================================
echo.

REM Buscar Python 3
where python3 >nul 2>&1
if %errorlevel%==0 (
    set PYTHON=python3
    goto :found
)
where python >nul 2>&1
if %errorlevel%==0 (
    set PYTHON=python
    goto :found
)
echo [ERROR] Python no encontrado. Instala Python desde https://python.org
pause
exit /b 1

:found
REM Obtener IP local
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /r "IPv4"') do (
    set IP=%%a
    set IP=!IP:~1!
    goto :gotip
)
:gotip
setlocal enabledelayedexpansion

echo Iniciando servidor...
echo.
echo  Abre en MOVIL (misma red WiFi):
echo.
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /r "Direcci.*IPv4\|IPv4 Address"') do (
    set RAWIP=%%a
    set RAWIP=!RAWIP: =!
    echo    http://!RAWIP!:8000/ginkana.html
)
echo.
echo  Abre en este ORDENADOR:
echo    http://localhost:8000/ginkana.html
echo.
echo ============================================
echo  Pulsa Ctrl+C para detener el servidor
echo ============================================
echo.
%PYTHON% -m http.server 8000
pause
