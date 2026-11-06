# Investigacion C2-DECT Lite - ordenado por carpeta

Raiz ejecutable: `INICIO.bat` / `ejecutar.py` en la raiz del repo.

## Estructura
- `INICIO.bat`, `ejecutar.py` - entrada principal (doble clic, sin admin)
- `docs/` - informes 00 a 21, plan, resultados, resumen 1 pagina, lab admin, instalacion
- `reglas/` - `reglas.yar`, `sigma_beaconing_periodico.yml`, `test_reglas.py`
- `scripts/` - analizadores y validadores: `analizar_*.py`, `validar_*.py`, `emular_*.py`, `comparar_*.py`, `ja3_*.py`, `medicion_*.py`, `generar_*.py`, `run_*.ps1`
- `datos/` - resultados versionados: CSV, resumenes, pos_*.txt, ejemplo lua
- `.github/workflows/` - CI GitHub Actions
- `tools/`, `validacion_dinamica/`, `fase2_dinamico/`, `escala_dinamica/`, `datasets_externos/` - dinamicos, gitignored, se regeneran/descargan

## Ejecutar todo
```powershell
.\INICIO.bat
# o
py ejecutar.py
```

## Fuente verificada
`Desktop\test\c2-dect-lite-2.0.0` - agent/catalog.go, transport.go, scripting.go

Solo lab propio. Sin payload real.
