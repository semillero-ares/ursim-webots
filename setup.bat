REM Ensure Python is installed
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

REM Create the docker network if it doesn't exist
docker network inspect dockernet >nul 2>&1
if errorlevel 1 (
    docker network create -d bridge --subnet 192.168.0.0/24 --gateway 192.168.0.1 dockernet
)
docker network inspect dockernet

REM Docker compose up
docker-compose up -d --compose-file ursim/compose.yml