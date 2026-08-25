@echo off
setlocal enabledelayedexpansion

:: Define ANSI Color Escape Codes
set "ESC="
set "GREEN=%ESC%[92m"
set "YELLOW=%ESC%[93m"
set "RED=%ESC%[91m"
set "CYAN=%ESC%[96m"
set "RESET=%ESC%[0m"

echo %CYAN%========================================%RESET%
echo %CYAN%Checking System Prerequisites%RESET%
echo %CYAN%========================================%RESET%
echo.

:: 1. Check Python in PATH
python --version >nul 2>&1
if !errorlevel! equ 0 (
    echo %GREEN%[OK] Python is in PATH:%RESET%
    python --version
) else (
    echo %YELLOW%[WARNING] Python was not found in your system PATH!%RESET%
    echo           Please install Python or add it to your environment variables.
)

echo.

:: 2. Check if Docker Desktop process is running
tasklist /fi "imagename eq Docker Desktop.exe" 2>NUL | find /i "Docker Desktop.exe" >nul
if !errorlevel! equ 0 (
    echo %GREEN%[OK] Docker Desktop is running.%RESET%
) else (
    echo %YELLOW%[WARNING] Docker Desktop is NOT running!%RESET%
    echo           Please start Docker Desktop before proceeding.
)

echo.
echo %CYAN%========================================%RESET%
echo %CYAN%Updating Pip and Installing Requirements%RESET%
echo %CYAN%========================================%RESET%
echo.

:: Update pip and install required packages
python -m pip install --upgrade pip
if !errorlevel! neq 0 (
    echo %YELLOW%[WARNING] Pip upgrade failed or was interrupted.%RESET%
)

python -m pip install -r requirements.txt
if !errorlevel! equ 0 (
    echo %GREEN%[OK] Python dependencies installed successfully.%RESET%
) else (
    echo %RED%[ERROR] Failed to install requirements from requirements.txt.%RESET%
)

echo.
echo %CYAN%========================================%RESET%
echo %CYAN%Starting Docker Containers%RESET%
echo %CYAN%========================================%RESET%
echo.

:: Docker compose up
if exist "pick-and-place-UR5e" (
    cd pick-and-place-UR5e
    echo %CYAN%Navigated to pick-and-place-UR5e directory.%RESET%
    echo.
    
    :: Try docker compose, fall back to docker-compose
    docker compose up -d || docker-compose up -d
    
    if !errorlevel! equ 0 (
        echo.
        echo %GREEN%[OK] Docker containers launched successfully!%RESET%
    ) else (
        echo.
        echo %RED%[ERROR] Failed to bring up Docker containers.%RESET%
    )
) else (
    echo %RED%[ERROR] Directory "pick-and-place-UR5e" not found!%RESET%
)

echo.
echo %CYAN%========================================%RESET%
pause