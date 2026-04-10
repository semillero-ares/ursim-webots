@echo off
REM Setup script for the project
REM Update pip and install required packages
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

REM Create the docker network if it doesn't exist
docker network inspect dockernet >nul 2>&1
if errorlevel 1 (
    docker network create -d bridge --subnet 172.19.0.0/24 --gateway 172.19.0.1 dockernet
)
docker network inspect dockernet

REM Docker compose up
cd pick-and-place-UR5e
docker-compose up -d

REM Pause to view any messages
pause
