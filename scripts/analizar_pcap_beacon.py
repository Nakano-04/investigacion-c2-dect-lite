#!/usr/bin/env python3
"""
Analizador defensivo de PCAP para beaconing en lab.
No ejecuta ni genera tráfico. Solo lee un PCAP ya capturado en lab aislado
y calcula estadísticas de intervalos entre paquetes de un flujo dado.

Uso:
  python analizar_pcap_beacon.py captura.pcap --ip 127.0.0.1 --port 8443

Requiere: pip install scapy
Salida: intervalo medio, desviación, jitter %, conteo, tamaño medio.
"""
import argparse
import statistics
import sys

def main():
    p = argparse.ArgumentParser(description="Estadísticas de beaconing en PCAP de lab")
    p.add_argument("pcap", help="Archivo PCAP capturado en lab")
    p.add_argument("--ip", default="127.0.0.1")
    p.add_argument("--port", type=int, default=8443)
    args = p.parse_args()

    try:
        from scapy.all import rdpcap, IP, TCP, UDP
    except ImportError:
        print("Falta scapy: pip install scapy", file=sys.stderr)
        sys.exit(1)

    pkts = rdpcap(args.pcap)
    times = []
    sizes = []
    for pkt in pkts:
        if IP not in pkt:
            continue
        if pkt[IP].dst != args.ip and pkt[IP].src != args.ip:
            continue
        sport = dport = None
        if TCP in pkt:
            sport, dport = pkt[TCP].sport, pkt[TCP].dport
        elif UDP in pkt:
            sport, dport = pkt[UDP].sport, pkt[UDP].dport
        else:
            continue
        if args.port not in (sport, dport):
            continue
        times.append(float(pkt.time))
        sizes.append(len(pkt))

    print(f"Paquetes coincidentes: {len(times)}")
    if len(times) < 3:
        print("Insuficientes paquetes para calcular beaconing.")
        return

    times.sort()
    intervals = [b - a for a, b in zip(times, times[1:])]
    mean_i = statistics.mean(intervals)
    stdev_i = statistics.stdev(intervals) if len(intervals) > 1 else 0.0
    jitter_pct = (stdev_i / mean_i * 100) if mean_i else 0.0
    mean_sz = statistics.mean(sizes)

    print(f"Intervalo medio: {mean_i:.2f}s")
    print(f"Desviación: {stdev_i:.2f}s")
    print(f"Jitter estimado: {jitter_pct:.1f}%")
    print(f"Tamaño medio paquete: {mean_sz:.1f} bytes")
    print(f"Intervalos: {[round(x,2) for x in intervals]}")
    print("\nInterpretación defensiva:")
    print("- Jitter bajo (<10%) sugiere beacon fijo.")
    print("- Jitter 20-40% es compatible con jitter uniform/activity del framework.")
    print("- Tamaño muy constante sugiere beacon, no navegación normal.")

if __name__ == "__main__":
    main()


