# Métricas amplias y comparación con baselines

Fecha: 2026-11-06 - respuesta a crítica 3

## Comparación vs baselines ingenuas (set mini 6 limpios / 4 positivos)
| Regla | TP/4 | FP/6 | Precisión |
|-------|------|------|-----------|
| baseline solo "Shell" | 1 | 1 | 0.50 |
| baseline solo "http" | 1 | 1 | 0.50 |
| nuestras reglas v1.1 | 4 | 0 | 1.00 |

Script: `comparar_reglas.py` - exige combinación de strings, baja FP.

## Validación completa (set sintético 33/12)
- TP 12/12, TN 33/33, FP 0, FN 0, precisión 1.0, recall 1.0
- Prueba ciega: TP 12, TN 33, FP 0, FN 0
- Script: `validar_completa.py`, detalle en `resultados_detalle.csv`

## Ruido/proxy/TLS simulados
- `emular_ruido_proxy_tls.py`: PCAP con 60 beacon + 208 ruido (DNS 53, HTTP 80, TLS 443)
- Filtro por IP/puerto aísla beacon 100% en sintético.
- En real: TLS cifra contenido, proxy oculta destino, solo metadata + EDR/Zeek detecta. Ver crítica 1 en `17_CRITICAS_Y_MEJORAS.md`.

## Tests automatizados
- `test_reglas.py`: 5 tests unittest, todos OK (compilan, limpio no dispara, parcial no dispara Office, lua/vba positivos disparan)

## Limitación que permanece
Set sintético no es set real. Para SOC se necesita:
- 100+ archivos Office reales legítimos
- Tráfico real con EDR/proxy/TLS en VMs admin
- Benchmark contra reglas públicas (YARA-Forge, ET Open) en mismo set
