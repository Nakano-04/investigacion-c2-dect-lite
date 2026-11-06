# Medición real localhost - RUN-009 (práctica, no teórica)
Fecha: 2026-11-06
Modo: local sin admin, tráfico HTTP real a 127.0.0.1:18080

## Qué se ejecutó de verdad
- Servidor HTTP benigno en 127.0.0.1:18080 (Python portable, hilo)
- Cliente HTTP benigno: 20 peticiones reales con intervalos del modelo activity (base 2s demo)
- Medición real de timestamps, HTTP 200 y RTT en ms
- CSV: `fase2_emulacion_localhost/medicion_real_localhost.csv`

## Resultados reales
- 20/20 HTTP 200, RTT 0-33ms
- Intervalo medio real: 2.03s, SD 1.90s, Jitter 93.9%
- Coincide con modelo activity (cola derecha, jitter alto) - no es cálculo teórico, es tiempo real medido.

## Diferencia vs RUN-007
RUN-007 fue modelo matemático + PCAP sintético.
RUN-009 es tráfico real localhost medido en tiempo real con el mismo modelo de intervalos.

## Para VM admin real
Instalador ya descargado y verificado por winget:
`C:\Users\BALDEONSARMIENTOLUIS\AppData\Local\Temp\WinGet\Oracle.VirtualBox.7.2.22\VirtualBox-7.2.22-175245-Win.exe`
Solo falta que el usuario lo ejecute como administrador (doble clic > Sí en UAC) - el agente no puede elevar permisos por seguridad.
Tras eso: crear vboxnet0 y VMs según `lab_admin_real/01_GUIA_INSTALACION_ADMIN.md`

