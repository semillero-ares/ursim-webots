@echo off

:: Try running python --version silently
python --version >nul 2>&1

:: Check the exit code of the previous command (0 = success)
if %errorlevel% equ 0 (
    echo [OK] Python is installed and configured in your PATH.
    python --version
) else (
    echo [WARNING] Python was not found in your system PATH!
    echo Please install Python or add its installation folder to your PATH environment variable.
    pause
)

:: Update pip and install required packages

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

:: Docker compose up
cd pick-and-place-UR5e
:: Try docker compose, catch with docker-compose
docker compose up -d || docker-compose up -d

:: Pause to view any messages
pause