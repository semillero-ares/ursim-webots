# Problemas Comunes

## Fallo en el setup.bat

Si por algun motivo falla la ejecución del `setup.bat` (este archivo está pensado para funcionar en Windows.) podras correr el simulador haciendo los pasos que debería hacer el archivo ejecutable. 

### Instalación de paquetes de Python

```sh
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```
### Creación de la red virtual

```sh
docker network create -d bridge --subnet 192.168.0.0/24 --gateway 192.168.0.1 dockernet
```

### Activación del contenedor

```sh
cd ursim
docker-compose up -d
```