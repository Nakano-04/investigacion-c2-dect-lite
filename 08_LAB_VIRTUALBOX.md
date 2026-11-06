# Lab en Oracle VM VirtualBox — instalación y VMs

Fecha: 2026-11-06
Estado instalación automática: fallida 2 veces
- Intento 1: SSL error en fuente msstore (winget)
- Intento 2: 0x800704c7 El usuario ha cancelado la operación (UAC / elevación)

## Modo portable elegido por el usuario (2026-11-06)
- Se descargó `tools/VirtualBoxPortable/Portable-VirtualBox_Starter.exe` desde vbox.me
- No se ejecutó automáticamente. Requiere ejecución manual como administrador para drivers temporales.
- Ver `tools/VirtualBoxPortable/README_PORTABLE.md`
- Limitación: versión antigua (6.4.10), puede fallar en Windows moderno. Alternativa: instalador oficial 7.2.22.

## Instalación manual (recomendada)
1. Descargar de https://www.virtualbox.org/wiki/Downloads
   - Windows Hosts, versión 7.x (misma versión que Extension Pack)
2. Ejecutar como administrador, aceptar drivers de red virtual
3. Reiniciar si lo pide
4. Verificar: `VBoxManage --version` en PowerShell

Alternativa con winget ya descargado:
El instalador 7.2.22 se descargó y verificó hash, pero no se elevó.
Si quieres reintentar, hazlo en PowerShell como administrador y acepta el UAC.

## Red Host-Only
- VirtualBox > Archivo > Administrador de red de host
- Crear `Host-Only Ethernet Adapter` -> `vboxnet0`
- IPv4: `192.168.56.1/24`
- DHCP desactivado (IPs fijas en VMs para medición)

## VM 1: lab-server
- OS sugerido: Ubuntu Server 24.04 LTS ligero o Debian 12
- RAM: 2 GB, CPU: 1-2, Disco: 20 GB dinámico
- Red: Host-Only, IP fija `192.168.56.10/24`, puerta `192.168.56.1`
- Sin NAT para corridas (solo para instalar paquetes, luego desconectar)
- Instalar: Go 1.21+ si se compila en lab, git, curl, Wireshark/tcpdump
- Snapshot: `lab-server-base`

## VM 2: lab-victima
- OS: Windows 10/11 (licencia de prueba / eval)
- RAM: 4 GB, CPU: 2, Disco: 40 GB dinámico
- Red: Host-Only, IP fija `192.168.56.20/24`
- Instalar: Sysmon (config SwiftOnSecurity), Wireshark, oletools (pip), YARA, Office con macros según hipótesis
- Desactivar actualizaciones automáticas durante corrida
- Snapshot: `lab-victima-base`

## Recursos del host
- RAM total detectada: 16 GB
- Recomendado: cerrar programas pesados, 2+4 GB para VMs deja margen para host
- Disco C: verificar espacio libre antes de crear discos

## Checklist post-instalación
- [ ] VirtualBox abre sin error de drivers
- [ ] vboxnet0 visible con 192.168.56.1
- [ ] VMs hacen ping entre sí (56.10 <-> 56.20)
- [ ] VM víctima NO tiene ruta a internet durante corrida
- [ ] Snapshots creados
- [ ] Sysmon/PCAP/YARA operativos en víctima

## Uso en la investigación
- Fase 2: server en lab-server, agent en lab-victima, solo Host-Only
- Fase 3: Office benigna en lab-victima, listener local en lab-server
- Cada corrida: anotar en 04_RUN_LOG.md, capturar, exportar evidencia, revertir snapshot
