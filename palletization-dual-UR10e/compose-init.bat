@echo off
setlocal enabledelayedexpansion

:: Define ANSI Color Escape Codes
set "ESC="
set "GREEN=%ESC%[92m"
set "RED=%ESC%[91m"
set "CYAN=%ESC%[96m"
set "RESET=%ESC%[0m"

echo %CYAN%========================================%RESET%
echo %CYAN%Starting Docker Container%RESET%
echo %CYAN%========================================%RESET%
echo.

:: Try docker compose, fall back to docker-compose
docker compose up -d || docker-compose up -d

:: Check execution result
if !errorlevel! equ 0 (
    echo.
    echo %GREEN%[OK] Container started successfully!%RESET%
) else (
    echo.
    echo %RED%[ERROR] Failed to start container.%RESET%
)

echo.
echo %CYAN%========================================%RESET%
pause