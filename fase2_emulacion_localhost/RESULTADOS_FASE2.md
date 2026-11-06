# Fase 2 — Emulación localhost de timing (modelo, sin ejecutar agent real)
Fecha: 2026-11-06
Fuente lógica: agent/jitter.go (uniform/activity, diurnalFactor, shapeFactor, backoff)

## Escenarios 24h
- uniform_10s_30pct_dia: n=8638 beacons/24h, media=10.00s, sd=1.72s, jitter%=17.2%, min=7.00s, max=13.00s
- activity_10s_dia: n=5128 beacons/24h, media=16.85s, sd=11.96s, jitter%=71.0%, min=2.50s, max=40.00s
- activity_10s_noche: n=5176 beacons/24h, media=16.69s, sd=11.86s, jitter%=71.0%, min=2.50s, max=40.00s
- none_10s_fijo: n=8640 beacons/24h, media=10.00s, sd=0.00s, jitter%=0.0%, min=10.00s, max=10.00s
- uniform_60s_30pct: n=1442 beacons/24h, media=59.94s, sd=10.28s, jitter%=17.1%, min=42.00s, max=77.98s
- backoff base 10s fallos 1-10: [10, 20, 40, 80, 160, 300, 300, 300, 300, 300] (techo 300s)
- PCAP sintético generado: beacon_sintetico_activity_10s.pcap (200 paquetes, 127.0.0.1:8443, actividad 10h)

## Interpretación defensiva
- uniform 30% sobre 10s: intervalo 7-13s, jitter ~17% (editable). Detectable por periodicidad con ventana de ±30%.
- activity día (9-18h, factor 1.0): similar a uniform pero con cola derecha (shape hasta 3.2), media mayor, jitter más alto.
- activity noche (factor 2.4): intervalos ~2.4x, menos beacons, patrón diurno detectable por cambio de tasa día/noche.
- none: intervalo fijo 10s, jitter 0% — trivialmente detectable por periodicidad perfecta.
- backoff: tras fallos, 10,20,40,80,160,300s... — patrón exponencial reconocible en logs.

## Detección recomendada
- No buscar un solo intervalo, buscar distribución + cambio diurno + destino único + tamaño constante.
- Sigma plantilla en sigma_beaconing_periodico.yml (conteo en ventana) + análisis PCAP offline con analizar_pcap_beacon.py.
- En producción: Zeek/Suricata con ventana temporal, no solo conteo.

## Limitación
Emulación del modelo matemático, no ejecución del agent/server real (sin Go en host, sin admin).
Para evidencia con tráfico real, ejecutar e2e en lab aislado y re-analizar PCAP con el mismo script.
