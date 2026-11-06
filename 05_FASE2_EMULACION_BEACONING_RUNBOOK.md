# Fase 2 — Emulación de beaconing (lab aislado, medición)

Objetivo: medir periodicidad, jitter y detección del transporte de simulación
sin ejecutar nada en el host principal.

## Pre-requisitos
- [ ] 2 VMs host-only: `lab-server` y `lab-victima`, snapshots limpios
- [ ] Reloj sincronizado, PCAP listo en interfaz host-only de `lab-victima`
- [ ] Sysmon + EDR/Defender activos en `lab-victima`
- [ ] Autorización escrita del lab
- Ver `01_CHECKLIST_LABORATORIO.md`

## Procedimiento de medición (alto nivel)
1. Anotar hora inicio y snapshot ID en `04_RUN_LOG.md` (nueva corrida)
2. En lab, levantar server y agent SOLO dentro de la red host-only
   usando el harness del propio repo (`scripts/e2e.ps1`) como referencia
   de checks esperados: health, login, registro, task sysinfo, gate de impacto,
   audit chain.
3. Capturar PCAP durante 5-10 minutos de beaconing normal.
4. Detener, exportar PCAP, revertir snapshot.
5. Analizar PCAP con `analizar_pcap_beacon.py`:
   - intervalo medio, desviación, jitter %
   - tamaño medio de paquetes, % UDP/TCP, destino único local
   - estimación de backoff si hubo fallos
6. Rellenar `02_PLANTILLA_MEDICION.md`:
   - ¿Detectó EDR? ¿tiempo?
   - ¿Aparece el beacon como periódico en PCAP?
   - ¿Se creó `~/.c2-dect-lite/agent.json`? (verificar en VM antes de revertir)

## Métricas a registrar
| Métrica | Esperado (código) | Medido en lab | Gap |
|---------|-------------------|---------------|-----|
| Sleep base | 10s defecto | | |
| Jitter | 30% activity | | |
| Backoff máx | 5 min | | |
| Timeout comando | 20s | | |
| Watchdog tarea | 90s | | |
| Rotación clave | 200 beacons | | |
| Tareas por beacon | 1 | | |

## Impacto a documentar
- Confidencialidad: solo metadatos visibles sin TLS, contenido cifrado
- Integridad: cambios limitados a comandos write sin gate
- Disponibilidad: watchdog evita cuelgue por `ps`/tasklist lento
- Detección: periodicidad + destino local + archivo de estado

## Criterio de cierre
PCAP + logs Sysmon + plantilla completada + snapshot revertido.
No se deja server/agent corriendo tras la corrida.
