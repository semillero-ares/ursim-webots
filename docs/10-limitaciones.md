# Limitaciones del simulador

A continuación listamos la limitaciones con las que nos encontraremos al usar webots con el ursim:

## Sin acceso a las entradas en el URSIM

El simulador URSIM no nos permite modificar las entradas que en el sistema real recibirian información del entorno. Para superar esta limitación enviamos información desde Webots a registros dentro del URSIM. 

Los archivo de instalación ya tienen configurados los nombres entonces se pueden implementar los programas con dichos nombres, y en caso de llevar el programa al robot real se puede simplemente cambiar a donde apuntan dichos nombres. 

## Sin retorno de choque

En el robot real la interfaz de control, al detectar un contacto o choque, para inmediatamente la simulación. En el simulador con URSIM no podemos enviar información del contacto y simular el _"paro de emergencias"_. 