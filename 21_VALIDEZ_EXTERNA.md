# Validez externa - datasets públicos, JA3/JA4 y agente real

Fecha: 2026-11-06

## 1. Dataset público C2 - malware-traffic-analysis.net
- PCAP: `2026-02-28-traffic-analysis-exercise.pcap` (6.58 MB, NetSupport Manager RAT)
- Fuente: https://www.malware-traffic-analysis.net/2026/02/28/ - zip con password `infected_20260228`
- Análisis con `analizar_dataset_externo.py` (scapy portable):
  - 15512 paquetes, host infectado 10.2.28.88 (14673 pkts), C2 45.131.214.85 (550 pkts, puerto 443)
  - Beaconing real C2: 276 paquetes, media 56.9s, SD 13.6s, jitter 24.0%, min 0, max 60.3s
  - Comparación con modelo: uniform base 60s jitter 30% predice media 60s jitter 17% - real 60s/24% está en rango, valida modelo fuera de sintético.
  - Hallazgo TLS: flujo C2 NO es TLS ClientHello, es HTTP POST (`POST http://45.131.214.85/fake...`) sobre 443. JA3 = 0 para C2.
  - JA3 benigno TLS (otros 443): 152 ClientHello analizados con `ja3_analizar.py`, top JA3 benignos listados. JA3 separa benigno, pero no detecta este C2 porque no usa TLS.
  - Conclusión: hace falta telemetría HTTP (método/Host/URI) + timing, no solo JA3. Proxy TLS no ayudaría si no hay TLS.

## 2. Dataset público TQH-C2 (Zenodo 21435571)
- Features: `TQH-C2_features.zip` (17.6 MB, Parquet con JA4/JA4S, etiquetas ATT&CK)
- Grid: 3 perfiles x 4 intervalos (30/300/1800/3600s) x 3 jitter (0/30/70%) - idéntico a nuestro modelo.
- Análisis con `analizar_tqh.py` (pyarrow/pandas):
  - A_i30_j30 (Sliver TLS): 4617 filas, benign 2904 / malicious 1601. JA4 top benign `t13d3113h2_e8f1e7e78f70_ce5650b735ce` (2958) vs malicious `t13i131000_f57a46bbacb6_e5728521abd4` (1599) - JA4 separa perfecto en este testbed.
  - A_i300_j30: malicious 907, JA4 malicious mismo fingerprint 907 casos.
  - C_i30_j30 (Mythic HTTP): JA4 nulos (0) porque no es TLS, igual que MTA.
- Conclusión: JA4 es telemetría válida tras proxy TLS para Sliver, inútil para HTTP-only C2. Timing + tamaño (orig_bytes ~2550 malicious vs benign) complementa.

## 3. Proxy TLS / JA3 - implementación
- `ja3_analizar.py`: calcula JA3 (MD5 de version,ciphers,extensions,curves,pointformats) desde ClientHello en PCAP, sin Zeek.
- En MTA: 152 JA3 benignos extraídos, 0 C2 (por HTTP). Demuestra límite de JA3.
- En TQH: JA4 ya viene etiquetado en Parquet, demuestra separación.
- Pendiente real: proxy de inspección TLS (mitmproxy/Zeek ssl.log) en VM admin con tráfico de fondo realista. Plan en `LAB_ADMIN_PLAN.md`.

## 4. Agente Go real en VM admin
- Estado: pendiente de VirtualBox admin por el usuario (instalador listo).
- Alternativa sin VM: Go portable por usuario + server/agent en localhost (127.0.0.1) - tráfico real loopback, sin admin, con comandos solo read.
- Al ejecutarse: capturar PCAP real, comparar intervalos reales vs modelo activity/uniform, comparar JA3/JA4 (transporte AES-GCM, no TLS estándar, JA3 no aplica), Sysmon/EDR.
- Ver `20_SIMULACION_A_EMULACION.md` RUN-010.

## Archivos (no versionados, datasets externos)
`datasets_externos/` está en `.gitignore` (PCAPs/Parquet grandes, licencia CC-BY / MTA). En git solo van scripts `analizar_dataset_externo.py`, `ja3_analizar.py`, `analizar_tqh.py` y este informe con hashes/resultados.
