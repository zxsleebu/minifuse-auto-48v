# Controlador CLI de Arturia MiniFuse

Un script de Python que permite activar y desactivar de forma programática la alimentación fantasma +48V, el modo directo mono y el modo instrumento en las interfaces de audio Arturia MiniFuse.

Este script está diseñado específicamente para Windows y utiliza la API oficial de los controladores de Arturia para controlar el hardware sin interrumpir las transmisiones de audio.

## Requisitos previos

1. **Python 3.x** (se requiere una versión de 64 bits).
2. **Controladores de Arturia MiniFuse** (deben estar instalados).
3. Arturia MiniFuse 1 o 2.

## Configuración

El script depende del DLL oficial de la API de Arturia (`arturiaminifuseusbaudioapi_x64.dll`).

Por defecto, el script busca el archivo en el directorio de instalación estándar del controlador:

`C:\Program Files\Arturia\MiniFuseAudioDriver\x64\arturiaminifuseusbaudioapi_x64.dll`

Si instalaste el software de Arturia en una ubicación personalizada, abre el script de Python y actualiza la variable `DLL_PATH` para que coincida con la ubicación en tu sistema.

## Uso

Abre una terminal (Símbolo del sistema o PowerShell) en el directorio donde se encuentra el script.

```bash
python main.py [power|mono|inst] [on/off] (opcional: número de canal para instrumento [1-2])
```

### Ejemplo

**Activar +48V:**

```bash
python main.py power on
```

**Desactivar instrumento en el canal 1:**

```bash
python main.py inst off 1
```

## Detalles técnicos

**El problema:** En Windows, los controladores de interfaces de audio (ASIO/WASAPI) toman el control exclusivo de la interfaz USB, lo que impide que métodos como `pyusb` o `libusb` funcionen, ya que generan un error "Access Denied" al no poder reclamar la interfaz mientras el audio está activo.

**La solución:** En lugar de intentar inyectar paquetes USB sin procesar mediante controladores de filtro, este script carga el DLL oficial de la API de Thesycon/Arturia y utiliza la función exportada `TUSBAUDIO_AudioControlRequestSet` para enviar solicitudes de control específicas al hardware mediante los selectores de control `0x04` (alimentación fantasma), `0x05` (direct mono) y `0x00` (instrumento).

## Solución de problemas

* **`Error: DLL no encontrado`**: Verifica que los controladores de Arturia MiniFuse estén instalados. Si están instalados en una ubicación no predeterminada, edita la variable `DLL_PATH` en el script.
* **`Error al cargar el DLL`**: Asegúrate de que estás utilizando una versión de Python de 64 bits, ya que el DLL de la API es de 64 bits.
* **`No se encontraron dispositivos`**: Verifica que el MiniFuse esté conectado y sea reconocido por el Administrador de dispositivos de Windows.
