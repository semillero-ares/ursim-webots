# Uso de Webots con URsim
Para poder usar el simulador de Webots con URsim, debemos realizar las siguientes instalaciones en nuestro computador:

- Como nuestros controladores en Webots usarán Python, instale [Python](https://www.python.org/downloads/).
- Instale también [Webots](https://cyberbotics.com/).
- Para ejecutar URsim usaremos contenedores; instale [Docker Desktop](https://www.docker.com/products/docker-desktop/).
- Para clonar el repositorio; instale [GIT](https://git-scm.com/install/windows).

![webots logo](/img/logo/webots.png){: width="52.63157894736842px"}
![python logo](/img/logo/python.svg){: width="50px"}
![docker desktop logo](/img/logo/docker-desktop.svg){: width="50px"}
![ur logo](/img/logo/ur.png){: width="50px"}

## Webots

Es un simulador de robots 3D que permite modelar, simular y probar robots y entornos de manera realista. Ofrece librerías de robots y dispositivos, soporte para sensores (cámaras, LIDAR, IMU, encoders), distintos motores de física, y herramientas de visualización, depuración y registro de datos. Webots permite desarrollar controladores en varios lenguajes (entre ellos Python, C/C++, Java y MATLAB) y conectarse con ROS, lo que facilita la integración con URsim. En este flujo de trabajo se usará Webots para diseñar y validar escenarios y controladores locales, y URsim (ejecutado en Docker) para emular el controlador del robot Universal Robots y verificar la compatibilidad antes de desplegar en hardware real.
