#!/usr/bin/env python3
"""Emulación defensiva del modelo de timing de c2-dect-lite.
Replica jitter.go (uniform/activity, diurnalFactor, shapeFactor, backoff)
y genera un PCAP sintético localhost para medir con analizar_pcap_beacon.py.
No usa ni ejecuta el agent/server real. Solo modela intervalos.
"""
import random, statistics
from datetime import datetime, timedelta
from pathlib import Path

random.seed(20261106)
ROOT = Path(__file__).resolve().parent
OUTDIR = ROOT / "fase2_dinamico"
OUTDIR.mkdir(exist_ok=True)

SHAPE = [0.00, 0.35, 0.70, 1.00, 1.55, 2.30, 3.20]

def diurnal(hour):
    if 9 <= hour < 18: return 1.0
    if 8 <= hour < 9 or 18 <= hour < 20: return 1.35
    if 20 <= hour < 23: return 1.8
    if hour >= 23 or hour < 6: return 2.4
    return 1.6

def shape_factor(u):
    n = len(SHAPE)-1
    if u <= 0: return SHAPE[0]
    if u >= 1: return SHAPE[n]
    pos = u*n; idx = int(pos)
    if idx >= n: return SHAPE[n]
    frac = pos-idx
    return SHAPE[idx] + (SHAPE[idx+1]-SHAPE[idx])*frac

def next_interval(base_ms, jitter_pct, mode, hour):
    if mode == "none" or jitter_pct == 0: return base_ms
    if mode == "activity":
        f = diurnal(hour) * shape_factor(random.random())
        f = max(0.25, min(4.0, f))
        return int(base_ms * f)
    # uniform
    delta = (random.random()*2-1) * (jitter_pct/100.0)
    return int(base_ms * (1+delta))

def backoff(base_sec, failures):
    failures = max(1, min(10, failures))
    sec = base_sec * (2 ** (failures-1))
    return min(300, max(1, sec))

def simulate(mode, start_hour, base_sec=10, jitter_pct=30, hours=24):
    base_ms = base_sec*1000
    t = datetime(2026,11,6, start_hour, 0, 0)
    end = t + timedelta(hours=hours)
    stamps = []
    intervals = []
    while t < end:
        stamps.append(t)
        iv = next_interval(base_ms, jitter_pct, mode, t.hour) / 1000.0
        intervals.append(iv)
        t += timedelta(seconds=iv)
    return stamps, intervals

# Escenarios
scenarios = [
    ("uniform_10s_30pct_dia", "uniform", 10, 10),
    ("activity_10s_dia", "activity", 10, 10),
    ("activity_10s_noche", "activity", 0, 10),
    ("none_10s_fijo", "none", 10, 10),
    ("uniform_60s_30pct", "uniform", 10, 60),
]

lines = []
for name, mode, start_h, base in scenarios:
    stamps, iv = simulate(mode, start_h, base_sec=base)
    mean = statistics.mean(iv); sd = statistics.stdev(iv) if len(iv)>1 else 0
    lines.append(f"- {name}: n={len(iv)} beacons/24h, media={mean:.2f}s, sd={sd:.2f}s, jitter%={sd/mean*100:.1f}%, min={min(iv):.2f}s, max={max(iv):.2f}s")

# Backoff
bo = [backoff(10, f) for f in range(1, 11)]
lines.append(f"- backoff base 10s fallos 1-10: {bo} (techo 300s)")

# Generar PCAP sintético activity 10s (manual, sin Ether/libpcap, sin admin)
try:
    import struct
    def ip_udp_packet(payload=b"BEACON-SIMULADO"):
        src = bytes([127,0,0,1]); dst = bytes([127,0,0,1])
        udp_len = 8+len(payload)
        ip_len = 20+udp_len
        # IP header sin checksum válido para análisis de timing (checksum 0)
        ip_hdr = struct.pack("!BBHHHBBH", 0x45, 0, ip_len, 0, 0, 64, 17, 0) + src + dst
        udp_hdr = struct.pack("!HHHH", 54321, 8443, udp_len, 0)
        return ip_hdr + udp_hdr + payload
    stamps, iv = simulate("activity", 10, base_sec=10, hours=1)
    pcap = OUTDIR / "beacon_sintetico_activity_10s.pcap"
    with open(pcap, "wb") as f:
        # global header: magic, ver 2.4, thiszone, sigfigs, snaplen, network=101 (raw IP)
        f.write(struct.pack("<IHHiIII", 0xa1b2c3d4, 2, 4, 0, 0, 65535, 101))
        t = 1762000000.0
        for _ in stamps[:200]:
            pkt = ip_udp_packet()
            sec = int(t); usec = int((t-sec)*1_000_000)
            f.write(struct.pack("<IIII", sec, usec, len(pkt), len(pkt)))
            f.write(pkt)
            t += next_interval(10000, 30, "activity", 10)/1000.0
    lines.append(f"- PCAP sintético generado: {pcap.name} ({len(stamps[:200])} paquetes, 127.0.0.1:8443, actividad 10h)")
except Exception as e:
    lines.append(f"- PCAP no generado: {e}")

report = "# Fase 2 — Emulación localhost de timing (modelo, sin ejecutar agent real)\nFecha: 2026-11-06\nFuente lógica: agent/jitter.go (uniform/activity, diurnalFactor, shapeFactor, backoff)\n\n## Escenarios 24h\n" + "\n".join(lines) + """

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
"""
(OUTDIR / "RESULTADOS_FASE2.md").write_text(report, encoding="utf-8")
print(report)
