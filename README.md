# Investigación C2-DECT Lite - todo a raíz, sin subcarpetas estáticas

Estructura plana: todos los informes, reglas y scripts en la **raíz del repo**.
Las carpetas de trabajo (`validacion_dinamica/`, `fase2_dinamico/`, `tools/`) son **dinámicas**, se generan al ejecutar los scripts y están en `.gitignore` - no se commitean.

## Raíz (archivos versionados)
- `00_*.md` a `16_*.md` - plan, inventario, resultados, informe final
- `LAB_ADMIN_*.md` - plan lab con VMs/admin
- `reglas.yar`, `sigma_beaconing_periodico.yml`
- `analizar_pcap_beacon.py`, `validar_completa.py`, `emular_beaconing.py`, `medicion_localhost_real.py`, `generar_muestra_benigna.py`
- `validar_yara.ps1`, `run_portable.ps1`
- `RESULTADOS_FASE2.md`, `RESUMEN_VALIDACION.md`, `resultados_detalle.csv`, `medicion_real_localhost.csv`
- `pos_*.txt`, `ejemplo_lua_benigno.lua`, `simulacion_vba_strings.txt`
- `.gitignore`, `PUBLICACION_README.md`

## Dinámicos (no versionados, se regeneran)
- `validacion_dinamica/` - sets limpio/positivo y prueba ciega
- `fase2_dinamico/` - PCAP sintético y resultados
- `tools/` - YARA/Python portables descargados por link

## Uso rápido (sin admin)
```powershell
.\tools\YARA\yara64.exe .\reglas.yar .\archivo
.\tools\PythonPortable\python.exe .\validar_completa.py
.\tools\PythonPortable\python.exe .\emular_beaconing.py
.\tools\PythonPortable\python.exe .\medicion_localhost_real.py
```

## Fuente verificada
`Desktop\test\c2-dect-lite-2.0.0` - agent/catalog.go, transport.go, scripting.go, scripts/e2e.ps1

Solo lab propio. Sin payload real.

