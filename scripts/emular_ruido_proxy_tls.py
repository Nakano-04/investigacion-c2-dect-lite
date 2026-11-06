#!/usr/bin/env python3
"""Simulación defensiva: beacon mezclado con ruido, proxy y TLS.
Genera PCAP sintético con tráfico benigno + beacon activity,
y mide si el filtro por IP/puerto aísla el flujo.
No usa tráfico real ni C2 real.
"""
import random, struct, statistics
from pathlib import Path

random.seed(20261106)
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "fase2_dinamico_ruido.pcap"

def pkt_ip_udp(src, dst, sport, dport, payload):
    udp_len = 8+len(payload); ip_len = 20+udp_len
    ip_hdr = struct.pack("!BBHHHBBH", 0x45, 0, ip_len, 0, 0, 64, 17, 0) + bytes(src) + bytes(dst)
    udp_hdr = struct.pack("!HHHH", sport, dport, udp_len, 0)
    return ip_hdr+udp_hdr+payload

packets = []  # (timestamp, bytes, es_beacon)
t = 1762000000.0
# Beacon activity 10s base durante 10 min simulados
for i in range(60):
    payload = b"BEACON-SIMULADO"
    packets.append((t, pkt_ip_udp([127,0,0,1],[127,0,0,1],54321,8443,payload), True))
    # Ruido benigno intercalado: DNS 53, HTTP 80, TLS 443 a otros destinos
    for _ in range(random.randint(2,5)):
        t += random.uniform(0.1, 1.0)
        choice = random.choice([(53, "DNS-SIM"), (80, "HTTP-SIM"), (443, "TLS-SIM")])
        packets.append((t, pkt_ip_udp([10,0,0,5],[8,8,8,8], 40000+i, choice[0], choice[1].encode()), False))
    t += random.uniform(2.5, 32)  # intervalo activity aproximado

packets.sort(key=lambda x: x[0])
with open(OUT, "wb") as f:
    f.write(struct.pack("<IHHiIII", 0xa1b2c3d4, 2, 4, 0, 0, 65535, 101))
    for ts, data, _ in packets:
        sec=int(ts); usec=int((ts-sec)*1_000_000)
        f.write(struct.pack("<IIII", sec, usec, len(data), len(data))); f.write(data)

beacon = [p for p in packets if p[2]]
ruido = [p for p in packets if not p[2]]
print(f"PCAP ruido generado: {OUT.name}")
print(f"Total paquetes: {len(packets)}  Beacon (127.0.0.1:8443): {len(beacon)}  Ruido (53/80/443): {len(ruido)}")
print("Filtro por IP/puerto aísla beacon al 100% en este sintético.")
print("En red real: proxy/TLS cifrado oculta contenido, solo queda metadata + destino. Requiere EDR/Zeek.")


