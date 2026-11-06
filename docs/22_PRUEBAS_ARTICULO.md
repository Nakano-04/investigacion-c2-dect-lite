# Pruebas del artículo - validación independiente, comparación, métricas y robustez

Fecha: 2026-11-06

## Prueba 1 - Validación independiente (prioritaria)
Set nuevo seed 20261107, vocabulario y plantillas Lua/VBA no usados para desarrollar reglas v1.1. Reglas congeladas.
- Limpio 20 -> FP 0, TN 20
- Positivo 10 -> TP 10, FN 0
- Precisión 1.000, Recall 1.000
Script: `scripts/prueba1_independiente.py`
Conclusión: las reglas generalizan fuera del set de desarrollo en este piloto sintético.

## Prueba 2 - Comparación con otras soluciones (mismas condiciones)
Mismo set independiente, 4 soluciones YARA:
| Solución | TP/10 | FP/20 | Precisión | Recall | F1 |
|----------|-------|-------|-----------|--------|----|
| nuestras v1.1 | 10 | 0 | 1.00 | 1.00 | 1.00 |
| baseline Shell | 2 | 0 | 1.00 | 0.20 | 0.33 |
| baseline http | 3 | 0 | 1.00 | 0.30 | 0.46 |
| baseline AutoOpen | 1 | 0 | 1.00 | 0.10 | 0.18 |
Script: `scripts/prueba2_comparacion.py`
Baselines de palabra suelta tienen recall bajo. Nuestras exigen combinación.

## Prueba 3 - Métricas estadísticas
| Set | TP | FN | TN | FP | Prec | Rec | F1 | FPR | Tiempo |
|-----|----|----|----|----|------|-----|----|-----|--------|
| independiente | 10 | 0 | 20 | 0 | 1.0 | 1.0 | 1.0 | 0.0 | 0.049s |
| validación completa | 12 | 0 | 33 | 0 | 1.0 | 1.0 | 1.0 | 0.0 | 0.045s |
| escala 500/200 | 200 | 0 | 500 | 0 | 1.0 | 1.0 | 1.0 | 0.0 | 0.129s |
Script: `scripts/prueba3_metricas.py`
Tiempo de detección beacon: por ventana temporal (ver emular_beaconing), no por intervalo único.

## Prueba 4 - Robustez ante variaciones
Matriz sintética intervalos 30/300/1800/3600 x jitter 0/30/70:
- jitter 0% -> jitter medido 0%, beacon perfecto
- jitter 30% -> jitter medido ~17%
- jitter 70% -> jitter medido ~35-42%
TQH-C2 real (Parquet): intervalos y jitter etiquetados coinciden con matriz, protocolos TCP/TLS/HTTP/QUIC.
MTA real: HTTP POST sobre 443, beacon 60s jitter 24%, JA3 nulo.
Conclusión robusta: timing funciona en todos los intervalos, JA4 solo en TLS, HTTP necesita metadata HTTP. Ninguna métrica sola es robusta; correlación timing+JA4/HTTP+tamaño sí.
Script: `scripts/prueba4_robustez.py`

## Limitación que permanece
Set independiente sigue siendo sintético. Validez externa real requiere macros Office reales, PCAPs corporativos con EDR/proxy/TLS y revisión por pares. Ver `19_REVISION_META_CRITICA.md` y `21_VALIDEZ_EXTERNA.md`.
