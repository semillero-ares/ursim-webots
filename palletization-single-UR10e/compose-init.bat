@echo off
echo Starting the container...
:: Try docker compose, catch with docker-compose
docker compose up -d || docker-compose up -d

:: Pause to view any messages
pause