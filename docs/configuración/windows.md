---
weight: 10
---
# Inicio rápido con Windows

Después de tener todos los programas anterior instalados, podremos empezar a usar URSIM con Webots. Lo primero que deberemos hacer será clonar el repositorio usando este comando en un terminal, pero antes de eso crearemos una carpeta en el PC donde queramos que los archivos estén. En nuestro caso usaremos `C:\ursim-webots` como ilustración.

Estando en la carpeta vamos a abrir un terminal. Hacemos clic derecho en el espacio vacío en la carpeta y en el menú desplegable escogemos `Abrir en Terminal`.

![Abrir en Terminal](img/windows/abrir-terminal.png){: class="img-center" title="Abrir en Terminal"}

Estando en el terminal vamos a ejecutar el siguiente comando:

```
git clone https://github.com/semillero-ares/ursim-webots.git .
```

Después de ejecutar el comando la carpeta debera tener alguno archivos, entre ellos uno llamado `setup.bat`. En el terminal vamos a ejecutar este archivo:

**IMPORTANTE:** Tener abierto el Docker Desktop, para que se haga el setup correctamente. 

```
.\setup.bat
```

También se puede ejecutar el setup, haciendo doble clic en el archivo `setup.bat` directamente. 

Si todo salió bien, deberemos tener un mensaje similar a este:

```
[+] Running 1/1
 ✔ Container ursim Started
Presione una tecla para continuar . . .
```

Y podremos acceder a URSIM a traves del navegador en este enlace [`http://localhost:6080/vnc.html`](http://localhost:6080/vnc.html). Si hubo algún problema revisar la sección de solución de [problemas comunes](60-problemas-comunes.md).