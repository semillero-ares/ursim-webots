# Empezando en ubuntu

Esta guía cubre los pasos para usar URSIM con Webots en **Ubuntu**. Los pasos difieren de la [guía principal](index.md) que está orientada a Windows.

Deberemos abrir un terminal y escribir lo siguiente:

```bash
curl -fsSL https://semillero-ares.github.io/ursim-webots/install.sh | bash
```

---

## Encontrar la IP del Mac para RealVNC

Si quieres conectarte al URSIM desde un dispositivo móvil usando RealVNC (ver [guía de VNC](10-vnc.md)), necesitarás conocer la IP de tu Mac en la red WiFi.

**Desde el terminal:**

```sh
ip a
```

> **IMPORTANTE:** En cada conexión a la red WiFi, **la dirección IP puede cambiar**.

---

## Detener e iniciar el simulador

Cuando termines de trabajar, puedes detener el contenedor de URSIM con:

```sh
cd ~/ursim-webots/ursim
docker compose down
```

Cuando quieras volver a trabajar, puedes iniciar el contenedor de URSIM con:

```sh
cd ~/ursim-webots/ursim
docker compose up -d
```

Accede al VNC desde el navegador aquí [`http://localhost:6080/vnc.html`](http://localhost:6080/vnc.html)