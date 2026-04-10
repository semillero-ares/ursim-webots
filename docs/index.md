# Tutorial de URSIM con Webots

Usar el URSIM con webots tiene la gran ventaja de tener un entorno completo de estudio para aprender de manipuladores y aprender a usar la interfaz gráfica de los robots de la empresa **Universal Robots** la cual nos ofrece el software URSIM sin un ambiente completo de simulación, ya que esta opción esta solo disponible si le compramos las formaciones ([aunque hay gratis](70-formacion-gratis.md)). Con este desarrollo del Semillero ARES, podremos tener el entorno completo aunque con [limitaciones](50-limitaciones.md).

Para poder usar el simulador de Webots con URsim, debemos realizar las siguientes instalaciones en nuestro computador:

1. [GIT](https://git-scm.com/install/windows), necesario para clonar el repositorio con todos los archivos de configuración de URSIM y el simulador en Webots. 

2. [Python](https://www.python.org/downloads/), lenguage de programación en el que desarrollamos los controladores del simulador Webots y la comunicación entre Webots y URSIM usando el protocolo de UR llamado RTDE. 

3. [Webots](https://cyberbotics.com/), es el motor de simulaciones que nos permite simular el robot y su interacción con el entorno. 

4. [Docker Desktop](https://www.docker.com/products/docker-desktop/), este motor nos permite instalar y correr fácilmente URSIM. 

![git logo](img/logo/git.svg){: class="logo img-center" title="Logo de Git"}
![python logo](img/logo/python.svg){: class="logo img-center" title="Logo de Python"}
![webots logo](img/logo/webots.png){: class="logo img-center" title="Logo de Webots"}
![docker desktop logo](img/logo/docker-desktop.svg){: class="logo img-center" title="Logo de Docker Desktop"}