# Lab con VMs y admin real - plan

Fecha: 2026-11-06
Objetivo: pasar del modo portable sin admin al modo completo con VMs aisladas para medir tráfico real, Sysmon y PCAP en vivo.

## Alcance
- Solo VMs propias, red Host-Only, sin internet durante corridas.
- Servidor de simulación solo en `lab-server`, agent solo en `lab-victima`.
- Nada de payload real para terceros, nada de exfiltración fuera del lab.

## Arquitectura
```
Host Windows (admin para instalar VirtualBox)
  vboxnet0 192.168.56.1/24 Host-Only
    lab-server  192.168.56.10  Linux (Ubuntu/Debian) 2GB
    lab-victima 192.168.56.20  Windows 10/11 4GB
```

## Fases admin
1. Instalar VirtualBox 7.2.22 como administrador (UAC). Verificado winget.
2. Crear red Host-Only vboxnet0.
3. Crear `lab-server`: Linux, Go 1.21+ para compilar server/agent en lab, git, tcpdump.
4. Crear `lab-victima`: Windows, Sysmon (driver, admin), Wireshark+Npcap (admin), oletools portable ya listo, Defender.
5. Snapshots base de ambas.
6. RUN-009: e2e real en lab (server+agent), captura PCAP en víctima, análisis con `analizar_pcap_beacon.py` (mismo script ya validado).
7. RUN-010: Office benigna en víctima con Sysmon 1/11, oletools previo, YARA.
8. Documentar en `04_RUN_LOG.md`, actualizar informe final a v1.1 con datos reales.

## Diferencia vs modo sin admin
| Aspecto | Sin admin (hecho) | Con admin (ahora) |
|---------|-------------------|-------------------|
| Aislamiento | Solo carpeta + localhost | VMs + snapshots + Host-Only |
| PCAP | Sintético offline | Real en vivo con Npcap |
| Sysmon | No (driver) | Sí |
| Tráfico C2 | Modelo matemático | Real del framework en lab |
| Set limpio | Sintético | Puedes ampliar con Office real de lab |

## Riesgos y control
- VirtualBox instala drivers/servicios de red (admin). Queda instalado en host.
- VMs consumen 6GB RAM + disco. Cerrar apps pesadas.
- Licencia Windows para víctima: usa imagen de evaluación / licencia propia.
- Destruir VMs al terminar si no se quieren conservar.

## Checklist de inicio
- [ ] Aceptar UAC en instalación VirtualBox
- [ ] `VBoxManage --version` OK en host admin
- [ ] vboxnet0 192.168.56.1 creado
- [ ] ISOs descargadas (Ubuntu, Windows eval) - links oficiales
- [ ] Snapshots base creados

