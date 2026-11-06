#!/usr/bin/env python3
"""JA3 fingerprint desde ClientHello TLS en PCAP (sin Zeek, sin proxy).
Calcula JA3 = MD5(version,ciphers,extensions,curves,pointformats)
para flujos a 443, separa C2 45.131.214.85 vs benigno.
Uso: py ja3_analizar.py datasets_externos/mta/...pcap
"""
import hashlib, struct, sys
from collections import Counter
from scapy.all import rdpcap, TCP, Raw

def ja3_from_hello(d):
    # TLS record: 1 byte type, 2 ver, 2 len, then handshake
    if len(d) < 43 or d[0] != 0x16: return None
    # Handshake header at offset 5: type(1), len(3), version(2), random(32)
    off = 5
    if d[off] != 0x01: return None
    ver = d[off+4:off+6]
    ver_str = f"{ver[0]},{ver[1]}"
    pos = off+38  # skip random
    # session id len
    sid_len = d[pos]; pos += 1+sid_len
    # cipher suites
    cs_len = struct.unpack("!H", d[pos:pos+2])[0]; pos+=2
    ciphers = [str(struct.unpack("!H", d[pos+i:pos+i+2])[0]) for i in range(0, cs_len, 2)]
    pos += cs_len
    # compression methods
    comp_len = d[pos]; pos += 1+comp_len
    # extensions
    exts = []
    if pos < len(d):
        ext_len = struct.unpack("!H", d[pos:pos+2])[0]; pos+=2
        end = pos+ext_len
        curves = []; points = []
        while pos+4 <= end and pos+4 <= len(d):
            etype, elen = struct.unpack("!HH", d[pos:pos+4]); pos+=4
            exts.append(str(etype))
            if etype == 10:  # supported_groups
                clen = struct.unpack("!H", d[pos:pos+2])[0]
                curves = [str(struct.unpack("!H", d[pos+2+i:pos+4+i])[0]) for i in range(0, clen, 2)]
            if etype == 11:  # ec_point_formats
                points = [str(b) for b in d[pos+1:pos+1+d[pos]]]
            pos += elen
    ja3_str = f"{ver_str},{','.join(ciphers)},{','.join(exts)},{','.join(curves)},{','.join(points)}"
    return hashlib.md5(ja3_str.encode()).hexdigest(), ja3_str

def main(pcap_path):
    pkts = rdpcap(pcap_path)
    c2 = Counter(); benign = Counter(); total=0
    for p in pkts:
        if TCP not in p or Raw not in p: continue
        d = bytes(p[Raw].load)
        if len(d)<5 or d[0]!=0x16 or d[1]!=0x03: continue
        r = ja3_from_hello(d)
        if not r: continue
        total+=1
        ja3,_ = r
        dst = p[TCP].dport
        if dst==443:
            # distinguir por IP destino si está
            try:
                dst_ip = p["IP"].dst
            except Exception:
                dst_ip="?"
            if dst_ip=="45.131.214.85": c2[ja3]+=1
            else: benign[ja3]+=1
    print(f"ClientHello analizados: {total}")
    print(f"JA3 C2 (45.131.214.85:443): {c2.most_common(5)}")
    print(f"JA3 benigno (otros 443): {benign.most_common(5)}")
    print("Conclusión: JA3 permite fingerprint sin descifrar, útil con proxy TLS / tráfico cifrado.")

if __name__=="__main__":
    main(sys.argv[1] if len(sys.argv)>1 else "datasets_externos/mta/2026-02-28-traffic-analysis-exercise.pcap")


