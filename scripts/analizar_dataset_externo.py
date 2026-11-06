#!/usr/bin/env python3
"""Análisis defensivo de dataset externo MTA PCAP.
Extrae: paquetes, protocolos, top IPs, TLS ClientHello (SNI, ALPN, JA3-like),
y beaconing por flujo src->dst:puerto (intervalos).
No ejecuta malware, solo lee PCAP.
"""
import hashlib, statistics
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PCAP = ROOT / "datasets_externos" / "mta" / "2026-02-28-traffic-analysis-exercise.pcap"

from scapy.all import rdpcap, IP, TCP, UDP, DNS, Raw
try:
    from scapy.layers.tls.all import TLSClientHello, TLS
    HAS_TLS = True
except Exception:
    HAS_TLS = False

pkts = rdpcap(str(PCAP))
print(f"PCAP: {PCAP.name} paquetes={len(pkts)} sha256={hashlib.sha256(PCAP.read_bytes()).hexdigest()[:16]}...")

ips = Counter(); ports = Counter(); protos = Counter()
flows = defaultdict(list)
tls_sni = Counter(); tls_versions = Counter(); ja3_like = Counter()

for p in pkts:
    if IP in p:
        ips[p[IP].src]+=1; ips[p[IP].dst]+=1
        flows[(p[IP].src, p[IP].dst)].append(float(p.time))
    if TCP in p:
        ports[p[TCP].dport]+=1; protos["TCP"]+=1
    if UDP in p:
        ports[p[UDP].dport]+=1; protos["UDP"]+=1
    if DNS in p:
        protos["DNS"]+=1
    if HAS_TLS and TLS in p:
        try:
            hello = p[TLSClientHello]
            # SNI
            for ext in hello.extensions:
                try:
                    if hasattr(ext, "servername"):
                        tls_sni[ext.servername]+=1
                except Exception: pass
            tls_versions[str(hello.version)]+=1
            # JA3-like: version, ciphers, extensions, curves, pointformats
            ciphers = ",".join(str(c) for c in hello.ciphers)[:80]
            ja3_like[ciphers]+=1
        except Exception:
            pass

print(f"Protocolos: {dict(protos)}")
print(f"Top IPs: {ips.most_common(8)}")
print(f"Top puertos dst: {ports.most_common(10)}")
print(f"TLS SNI: {tls_sni.most_common(10)}")
print(f"TLS versiones: {dict(tls_versions)}")
print(f"JA3-like (ciphers top): {ja3_like.most_common(3)}")

print("\nBeaconing por flujo (src->dst, n>=10):")
for (src,dst), times in sorted(flows.items(), key=lambda x: -len(x[1]))[:10]:
    if len(times) < 10: continue
    times.sort(); iv=[b-a for a,b in zip(times,times[1:])]
    if iv:
        m=statistics.mean(iv); sd=statistics.stdev(iv) if len(iv)>1 else 0
        print(f" {src} -> {dst} n={len(times)} media={m:.1f}s sd={sd:.1f}s jitter%={sd/m*100:.1f}% min={min(iv):.1f} max={max(iv):.1f}")

print("\nInterpretación: este PCAP es NetSupport Manager RAT a 45.131.214.85:443 según el ejercicio MTA. Comparar su beaconing/JA3 con nuestro modelo activity/uniform.")


