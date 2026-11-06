# De simulación a emulación

Fecha: 2026-11-06

## Diferencia en este proyecto
- **Simulación (hecha):** modelo matemático de jitter.go, PCAP sintético, sets YARA sintéticos, cliente HTTP benigno. Valida el pipeline, no el sistema real.
- **Emulación (pendiente):** ejecutar el sistema real - server + agent de C2-DECT Lite 2.0.0 - en VMs aisladas, con red real, Sysmon/EDR y Office real. Mide comportamiento real vs predicción de la simulación.

## Hipótesis a validar con emulación
H1: El jitter real medido en PCAP coincide con el modelo activity (~71% jitter, media ~16.8s base 10s).
H2: Sysmon/EDR detecta proceso hijo y archivo `~/.c2-dect-lite/agent.json` en emulación, no solo en simulación.
H3: YARA mantiene FP 0 en Office real de lab y detecta artefactos reales del agent compilado.
H4: Con proxy/TLS/ruido real, la detección por metadata sigue funcionando, la de contenido no.

## Requisitos para emulación (admin real)
- [ ] VirtualBox instalado como admin - instalador listo en `Temp\WinGet\Oracle.VirtualBox.7.2.22\VirtualBox-7.2.22-175245-Win.exe`
- [ ] vboxnet0 Host-Only 192.168.56.1/24
- [ ] lab-server (Linux, Go 1.21+) 192.168.56.10
- [ ] lab-victima (Windows, Sysmon, Wireshark+Npcap, Defender) 192.168.56.20
- [ ] Snapshots base de ambas
- [ ] Sin internet durante corridas

Ver: `LAB_ADMIN_PLAN.md`, `LAB_ADMIN_GUIA.md`

## Plan de emulación (RUN-010 y RUN-011)
### RUN-010 - Beaconing real
1. Server en lab-server, agent en lab-victima, solo Host-Only.
2. Capturar PCAP en víctima 10 min.
3. Analizar con `analizar_pcap_beacon.py` (mismo script ya validado en simulación).
4. Comparar: media/jitter real vs predicción simulación (16.85s / 71%).
5. Revisar Sysmon 1/11, EDR, archivo de estado, logs de auditoría del server.

### RUN-011 - Office real benigna
1. Muestra benigna en víctima (solo marcador, sin payload real).
2. oletools + YARA antes de abrir.
3. Abrir, Sysmon/EDR durante, PCAP.
4. Medir: MOTW, Vista protegida, proceso hijo, detección.

## Métricas de transición
| Métrica | Simulación | Emulación (objetivo) |
|---------|------------|----------------------|
| Jitter activity | 71% modelo | Medir real, error <20% |
| YARA FP | 0/33 y 0/500 sintético | FP en Office real lab |
| Tiempo detección EDR | No medido | Segundos/minutos reales |
| PCAP | Sintético 200 pkts | Real 10 min, ruido real |

## Qué no cambia
- Solo lab propio, sin payload real, sin evasión, sin terceros.
- El agente real solo en VMs de lab, con doble puerta de impacto respetada.

## Estado
Simulación completada (RUN-001 a RUN-009). Emulación lista en runbooks, bloqueada por instalación admin de VirtualBox por el usuario.
Al instalar VirtualBox y crear VMs, se ejecuta RUN-010/011 y se actualiza este informe a v2.0 con datos reales.
