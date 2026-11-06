# Instalación reproducible - sin admin

## Requisitos
- Windows 10/11, PowerShell, conexión para descargar portables
- Python 3.12 por usuario: `winget install --id Python.Python.3.12 -e --scope user`
- Git por usuario: `winget install --id Git.Git -e --scope user`
- GitHub CLI por usuario: `winget install --id GitHub.cli -e --scope user`

## Portables locales (sin admin)
- YARA 4.6.0: descargar zip de https://github.com/VirusTotal/yara/releases y descomprimir en `tools/YARA/`
- Python portable alternativo: embeddable zip de https://www.python.org/ftp/python/3.12.10/python-3.12.10-embed-amd64.zip en `tools/PythonPortable/`
- Paquetes: `py -m pip install oletools scapy`

## Ejecutar todo
```powershell
py -m unittest test_reglas -v
py validar_completa.py
py emular_beaconing.py
py emular_ruido_proxy_tls.py
py comparar_reglas.py
py medicion_localhost_real.py
```

## CI
GitHub Actions en `.github/workflows/validacion.yml` corre YARA + tests + validación en Ubuntu en cada push.

Importante: `reglas.yar` debe ser ASCII sin BOM. Si YARA dice "non-ascii character", reescribe con ASCII sin BOM.
