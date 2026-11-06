# Investigacion C2-DECT Lite - ordenado por carpeta

Raiz ejecutable: `INICIO.bat` / `ejecutar.py` en la raiz del repo.

## Estructura
- `INICIO.bat`, `ejecutar.py` - entrada principal (doble clic, sin admin)
- `docs/` - informes 00 a 22, plan, resultados, resumen 1 pagina, lab admin, instalacion
- `reglas/` - `reglas.yar`, `sigma_beaconing_periodico.yml`, `test_reglas.py`
- `scripts/` - analizadores y validadores: `analizar_*.py`, `validar_*.py`, `emular_*.py`, `comparar_*.py`, `ja3_*.py`, `medicion_*.py`, `generar_*.py`, `prueba*.py`, `run_*.ps1`
- `datos/` - resultados versionados: CSV, resumenes, pos_*.txt, ejemplo lua
- `.github/workflows/` - CI GitHub Actions
- `tools/`, `validacion_dinamica/`, `fase2_dinamico/`, `escala_dinamica/`, `datasets_externos/` - dinamicos, gitignored, se regeneran/descargan

## Ejecutar todo
```powershell
.\INICIO.bat
# o
py ejecutar.py
```

## Pruebas del articulo - matriz completa

### Prueba 1 - Validacion independiente (prioritaria)
Set nuevo seed 20261107, no usado para desarrollar reglas v1.1. Reglas congeladas.
| Set | TP | FN | TN | FP | Precision | Recall |
|-----|----|----|----|----|-----------|--------|
| Limpio 20 / Positivo 10 | 10 | 0 | 20 | 0 | 1.000 | 1.000 |
Script: `scripts/prueba1_independiente.py` - Detalle: `docs/22_PRUEBAS_ARTICULO.md`

### Prueba 2 - Comparacion con otras soluciones (mismas condiciones)
Mismo set independiente 20 limpios / 10 positivos.
| Solucion | TP/10 | FP/20 | Precision | Recall | F1 |
|----------|-------|-------|-----------|--------|----|
| nuestras v1.1 | 10 | 0 | 1.00 | 1.00 | 1.00 |
| baseline Shell | 2 | 0 | 1.00 | 0.20 | 0.33 |
| baseline http | 3 | 0 | 1.00 | 0.30 | 0.46 |
| baseline AutoOpen | 1 | 0 | 1.00 | 0.10 | 0.18 |
Script: `scripts/prueba2_comparacion.py`

### Prueba 3 - Metricas estadisticas
| Set | TP | FN | TN | FP | Precision | Recall | F1 | FPR | Tiempo |
|-----|----|----|----|----|-----------|--------|----|-----|--------|
| independiente 20/10 | 10 | 0 | 20 | 0 | 1.0 | 1.0 | 1.0 | 0.0 | 0.049s |
| validacion 33/12 | 12 | 0 | 33 | 0 | 1.0 | 1.0 | 1.0 | 0.0 | 0.045s |
| escala 500/200 | 200 | 0 | 500 | 0 | 1.0 | 1.0 | 1.0 | 0.0 | 0.129s |
Script: `scripts/prueba3_metricas.py`

### Prueba 4 - Robustez ante variaciones de trafico, protocolos y periodicidad
Matriz sintetica intervalos x jitter:
| Intervalo | Jitter 0% | Jitter 30% | Jitter 70% |
|-----------|-----------|------------|------------|
| 30s | media 30.0s jitter 0.0% | media 29.2s jitter 17.2% | media 31.0s jitter 38.3% |
| 300s | media 300.0s jitter 0.0% | media 297.2s jitter 16.7% | media 294.4s jitter 41.7% |
| 1800s | media 1800.0s jitter 0.0% | media 1767.2s jitter 17.9% | media 2033.2s jitter 34.3% |
| 3600s | media 3600.0s jitter 0.0% | media 3586.0s jitter 16.8% | media 3508.9s jitter 41.7% |
Protocolos: TLS Sliver A (JA4 separa benigno/malicious), HTTP Mythic C y MTA NetSupport (JA4 nulo, HTTP POST sobre 443), QUIC Merlin B.
Conclusion: timing funciona en todos los intervalos, JA4 solo en TLS, HTTP necesita metadata HTTP. Correlacion timing+JA4/HTTP+tamano es la robusta.
Script: `scripts/prueba4_robustez.py` + `scripts/analizar_tqh.py` + `scripts/analizar_dataset_externo.py`

## Validez externa
- MTA PCAP real: beacon 60s jitter 24% a 45.131.214.85, HTTP no TLS - ver `docs/21_VALIDEZ_EXTERNA.md`
- TQH-C2: JA4 separa Sliver TLS, grid intervalos/jitter identico al modelo
- CI externo GitHub Actions: verde en Ubuntu (cross-platform)

## Fuente verificada
`Desktop\test\c2-dect-lite-2.0.0` - agent/catalog.go, transport.go, scripting.go

Solo lab propio. Sin payload real.
