# Fase 2 — Emulación localhost de timing: resultados (RUN-007)
Fecha: 2026-11-06
Modo: local sin admin, sin ejecutar agent/server real (sin Go en host)

## Método
- Réplica exacta en Python portable de `agent/jitter.go`:
  - uniform: base*(1+delta), delta ±30%
  - activity: base * diurnalFactor(hora) * shapeFactor(u), clamp 0.25-4.0
  - diurnal: 1.0 (9-18h), 1.35, 1.8, 2.4 noche
  - shape: piecewise [0,0.35,0.70,1.00,1.55,2.30,3.20]
  - backoff: base*2^(fallos-1), techo 300s
- Script: `tools/emular_beaconing.py` (seed 20261106)
- PCAP sintético manual (sin Ether/libpcap): `fase2_emulacion_localhost/beacon_sintetico_activity_10s.pcap`
  200 paquetes IP/UDP 127.0.0.1:54321 -> 127.0.0.1:8443, payload BEACON-SIMULADO

## Escenarios 24h (base 10s salvo indicado)
| Escenario | Beacons/24h | Media | SD | Jitter% | Min-Max |
|-----------|-------------|-------|----|---------|---------|
| uniform 10s 30% día | 8638 | 10.00s | 1.72s | 17.2% | 7.00-13.00s |
| activity 10s día | 5128 | 16.85s | 11.96s | 71.0% | 2.50-40.00s |
| activity 10s noche | 5176 | 16.69s | 11.86s | 71.0% | 2.50-40.00s |
| none 10s fijo | 8640 | 10.00s | 0.00s | 0.0% | 10.00s |
| uniform 60s 30% | 1442 | 59.94s | 10.28s | 17.1% | 42-78s |

Backoff base 10s: 10,20,40,80,160,300,300,300,300,300

## Análisis PCAP sintético (analizar_pcap_beacon.py + scapy portable)
- Paquetes: 200
- Intervalo medio: 13.22s, SD 8.77s, Jitter estimado: 66.4%
- Tamaño medio: 43.0 bytes (constante)
- Coincide con modelo activity (~71% en 24h, variación por muestra de 1h)

## Interpretación defensiva
- uniform es fácilmente detectable por ventana ±30% sobre base.
- activity tiene cola derecha pesada y jitter alto, pero mantiene destino único, tamaño constante y cambio diurno — detectable por distribución, no por intervalo único.
- none es beacon perfecto, detección trivial.
- backoff exponencial es firma temporal reconocible tras fallos.

## Detección recomendada
- Sigma por conteo en ventana (plantilla existente) + análisis temporal (Zeek/Suricata) en producción.
- Correlacionar: proceso + archivo `~/.c2-dect-lite/agent.json` + endpoint `/agent/checkin` + beacon.

## Limitación honesta
Emulación matemática, no tráfico real del agent. Para evidencia real: correr e2e en lab aislado con Go portable en VM y re-analizar PCAP con el mismo script. El pipeline de medición ya está validado end-to-end (generación -> PCAP -> análisis).
