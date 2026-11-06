#!/usr/bin/env python3
"""Medición REAL localhost (sin admin, sin C2 real).
Servidor HTTP benigno en 127.0.0.1:18080 + cliente que envía
peticiones con intervalos del modelo jitter (base 2s reducida para demo).
Mide intervalos reales, RTT y guarda CSV. No es el agent de c2-dect-lite,
es un cliente HTTP benigno para validar el pipeline de medición.
"""
import csv, random, statistics, threading, time, urllib.request
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

random.seed(20261106)
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "medicion_real_localhost.csv"
OUT.parent.mkdir(exist_ok=True)

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.end_headers(); self.wfile.write(b"OK")
    def log_message(self, *a): pass

srv = HTTPServer(("127.0.0.1", 18080), H)
th = threading.Thread(target=srv.serve_forever, daemon=True); th.start()
print("Servidor benigno en 127.0.0.1:18080 iniciado")

SHAPE = [0.00,0.35,0.70,1.00,1.55,2.30,3.20]
def shape_factor(u):
    n=len(SHAPE)-1
    if u<=0: return SHAPE[0]
    if u>=1: return SHAPE[n]
    pos=u*n; idx=int(pos); frac=pos-idx
    return SHAPE[idx]+(SHAPE[idx+1]-SHAPE[idx])*frac

rows=[]; stamps=[]
start=time.time()
BASE=2.0  # 2s base para demo rápida (en real sería 10s)
for i in range(20):
    t0=time.time()
    try:
        with urllib.request.urlopen("http://127.0.0.1:18080/beacon-simulado", timeout=3) as r:
            code=r.status; body=r.read()
    except Exception as e:
        code=0; body=b""
    t1=time.time(); rtt=(t1-t0)*1000
    stamps.append(t0)
    rows.append([i+1, datetime.fromtimestamp(t0).isoformat(), f"{t0-start:.3f}", code, f"{rtt:.2f}"])
    print(f"[{i+1:02d}] {t0-start:.2f}s HTTP {code} RTT {rtt:.1f}ms")
    # intervalo activity día factor 1.0 * shape
    iv = BASE * max(0.25, min(4.0, 1.0*shape_factor(random.random())))
    time.sleep(iv)

srv.shutdown()
intervals=[b-a for a,b in zip(stamps, stamps[1:])]
with open(OUT, "w", newline="", encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["n","timestamp","t_rel_s","http","rtt_ms"]); w.writerows(rows)
mean=statistics.mean(intervals); sd=statistics.stdev(intervals)
print(f"\nMedición REAL completada: {len(rows)} peticiones")
print(f"Intervalo real medio: {mean:.2f}s  SD: {sd:.2f}s  Jitter: {sd/mean*100:.1f}%")
print(f"CSV guardado: {OUT}")


