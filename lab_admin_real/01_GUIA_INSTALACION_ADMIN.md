# Guía de instalación con admin real

## 1. VirtualBox (host)
- Instalador oficial 7.2.22 descargado por winget y verificado hash.
- Ejecutar como administrador, aceptar drivers.
- Verificar: abrir PowerShell como admin -> `VBoxManage --version`
- Extension Pack (misma versión) opcional para USB/red avanzada.

## 2. Red Host-Only
VirtualBox > Archivo > Administrador de red de host > crear vboxnet0 `192.168.56.1/24`
DHCP: desactivado. IPs fijas en VMs.

## 3. lab-server (Linux)
- Ubuntu Server 24.04 LTS ISO oficial: https://ubuntu.com/download/server
- 2GB RAM, 1-2 CPU, 20GB disco dinámico, red Host-Only
- IP fija: 192.168.56.10/24
- Paquetes: git, curl, tcpdump, Go 1.21+ (apt golang o tarball oficial)
- Copiar carpeta c2-dect-lite-2.0.0 a la VM (solo para lab)
- Snapshot: lab-server-base

## 4. lab-victima (Windows)
- Windows 10/11 ISO oficial Microsoft (eval / tu licencia)
- 4GB RAM, 2 CPU, 40GB disco, red Host-Only, IP 192.168.56.20
- Instalar como admin en la VM:
  - Sysmon: descargar de Microsoft Sysinternals, `sysmon.exe -i -n -h swift.xml` (config SwiftOnSecurity)
  - Wireshark: https://www.wireshark.org/download.html + Npcap (admin)
  - Office (para Fase Office) o solo oletools portable copiado
- Copiar `investigacion_c2_dect_lite/tools/` portable a la VM (YARA, Python, reglas)
- Snapshot: lab-victima-base

## 5. Prueba de conectividad
- Host ping 192.168.56.10 y .20
- lab-server ping lab-victima y viceversa
- lab-victima SIN internet: desconectar NAT, dejar solo Host-Only para corrida

## 6. Corridas (ver 05_FASE2... y 06_FASE3...)
- RUN-009 beaconing real: server en .10, agent en .20, PCAP en .20, análisis offline con script ya validado
- RUN-010 Office benigna: oletools + YARA antes, Sysmon durante, revertir snapshot después

## Limpieza
- Revertir snapshots tras cada corrida
- Al final: apagar VMs, exportar evidencia, borrar ISOs si se desea
