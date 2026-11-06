# Lab local sin admin — decisión 2026-11-06

El usuario pidió: todo local, sin admin, portable.
VirtualBox (instalado y portable) requiere admin para drivers/servicios, por lo que se descarta para este modo.

## Herramientas portables instaladas en carpeta local (sin admin, sin registro)

### YARA 4.6.0 portable
- Ubicación: `tools\YARA\yara64.exe`, `yarac64.exe`
- Fuente: https://github.com/VirusTotal/yara/releases/download/v4.6.0/yara-4.6.0-2443-win64.zip
- Verificado: `yara64.exe --version` -> 4.6.0, escanea `reglas.yar` OK

### Python 3.12.10 embeddable portable
- Ubicación: `tools\PythonPortable\python.exe`
- Fuente: https://www.python.org/ftp/python/3.12.10/python-3.12.10-embed-amd64.zip
- Configurado `python312._pth` con `import site` y `Lib\site-packages`
- pip portable instalado vía `get-pip.py` con `--target`
- Paquetes locales (sin admin): oletools 0.60.2, scapy 2.8.0, olefile, pyparsing, pcodedmp, msoffcrypto-tool, colorclass, cryptography, setuptools, wheel
- Verificado: `python.exe -m oletools.olevba --help` OK, `import scapy` 2.8.0 OK

## Qué se puede hacer sin admin
- [x] Análisis estático de Office con oletools (oleid/olevba) — no ejecuta macros
- [x] YARA portable contra archivos
- [x] Análisis PCAP con scapy portable (lee PCAP, no captura con Npcap)
- [x] Emulación localhost: server/agent como procesos de usuario en 127.0.0.1 (sin drivers)
- [ ] Captura PCAP en vivo con Wireshark/Npcap — requiere admin para driver, sustituir por logs de server/audit y timestamps de agent
- [ ] Sysmon — requiere admin para driver, sustituir por logs de proceso con PowerShell / Defender (sin instalar driver)
- [ ] Ejecutar macro Office — solo en carpeta aislada del proyecto, con muestra benigna, nunca en archivos reales

## Estructura portable
```
investigacion_c2_dect_lite/
  tools/
    YARA/yara64.exe
    PythonPortable/python.exe + Lib/site-packages/
    VirtualBoxPortable/ (descartado por admin, se conserva como referencia)
  reglas.yar
  analizar_pcap_beacon.py
  validar_yara.ps1 (actualizar ruta a yara64.exe)
```

## Comandos sin admin (PowerShell)
```powershell
# YARA
.\tools\YARA\yara64.exe .\reglas.yar .\ruta\archivo

# oletools
.\tools\PythonPortable\python.exe -m oletools.oleid .\muestra.docm
.\tools\PythonPortable\python.exe -m oletools.olevba .\muestra.docm

# PCAP (archivo ya capturado, no captura en vivo)
.\tools\PythonPortable\python.exe .\analizar_pcap_beacon.py captura.pcap --ip 127.0.0.1 --port 8443

# Wrapper (requiere Bypass por proceso, sin admin):
powershell -ExecutionPolicy Bypass -File .\tools\run_portable.ps1 yara .\reglas.yar .\archivo
```

## Límites honestos sin admin
- Sin aislamiento de VM: la emulación localhost corre en tu usuario. Solo usar comandos read, nunca impact sin consentimiento, y solo en carpeta de lab.
- Sin captura de red del sistema: usar logs de aplicación (server.out, agent.out, audit) en vez de PCAP en vivo.
- Para Fase 3 Office: solo estático. Si se ejecuta macro benigna, hacerlo fuera de documentos reales y con Defender activo.

## Borrado total
Borrar carpeta `investigacion_c2_dect_lite\tools\` deja el sistema limpio, sin desinstaladores.
