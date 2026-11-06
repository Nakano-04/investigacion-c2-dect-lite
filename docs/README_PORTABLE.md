# VirtualBox Portable - local, sin instalar

Descargado 2026-11-06 desde https://www.vbox.me/
Archivo: `Portable-VirtualBox_Starter.exe` (1.4 MB, starter)

## Importante (leído de vbox.me)
- Portable-VirtualBox NO modifica archivos de VirtualBox, los extrae del instalador oficial.
- Aunque es portable en archivos, **sí necesita permisos de administrador** la primera vez para instalar temporalmente drivers/servicios de red, y los retira al salir.
- Versión del launcher: 5.1.22 / VirtualBox 6.4.10 - es antigua. Puede tener problemas en Windows 11 / drivers modernos. Si falla, la alternativa es el instalador oficial 7.2.22 que ya descargó winget.

## Cómo usarlo (manual, como administrador)
1. Clic derecho en `Portable-VirtualBox_Starter.exe` > Ejecutar como administrador
2. Elige carpeta de extracción: esta misma carpeta `tools\VirtualBoxPortable\`
3. Ejecuta `Portable-VirtualBox.exe` de la carpeta extraída
4. Cuando pregunte por instalador: haz clic en "Download The Installation Files of VirtualBox" (descarga oficial)
5. Acepta drivers cuando lo pida (UAC)
6. Abre la GUI de VirtualBox portable

## Todo local
- VMs, discos (.vmdk/.vdi) y config se guardan en esta carpeta si configuras Home Directory a `.\VMs`
- Para borrar todo: cierra VirtualBox y borra la carpeta `tools\VirtualBoxPortable\`
- No queda entrada en Panel de Control

## Riesgo
- Proyecto de terceros (vbox.me / GitHub vboxme), no es oficial de Oracle.
- Solo descargar de vbox.me, no de sitios espejo raros.
- Escanea el starter con Defender antes de ejecutar.

## Alternativa si el portable falla por versión vieja
Usa el instalador oficial 7.2.22 que winget ya descargó y verificó:
`VirtualBox-7.2.22-175245-Win.exe`
Ese sí requiere instalación normal como administrador, pero es la versión soportada.

