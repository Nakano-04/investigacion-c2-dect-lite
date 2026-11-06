# Emulación y detección defensiva de C2-DECT Lite 2.0.0 y macros Office
## Informe técnico - investigación en laboratorio local sin administrador

**Fecha:** 2026-11-06
**Autor:** Equipo de investigación defensiva (lab local)
**Versión:** 1.0 - para publicación como informe técnico / repo de investigación
**Licencia:** CC-BY 4.0 para este informe. El framework analizado es Non-Commercial de su autor; no se redistribuye su código.

> **Aviso ético:** Investigación solo en laboratorio propio, red localhost, sin carga útil real, sin evasión, sin terceros. Herramientas portables en modo usuario, sin instalación en el sistema.

---

## Resumen ejecutivo
Se estudió la plataforma de simulación adversaria **C2-DECT Lite 2.0.0** (`Nakano-04/c2-dect-lite`) desde cero, en modo 100% local y sin administrador, para medir cómo se comporta su beaconing y qué artefactos deja, y derivar detecciones defensivas (YARA + Sigma).

Resultados principales:
- Inventario estático completo del framework (catálogo cerrado, transporte ECDH+AES-GCM, jitter, scripting Lua sandbox).
- Validación YARA piloto: **33 limpios / 12 positivos simulados, 0 FP, 0 FN, precisión y recall 1.0** en set sintético controlado. Prueba ciega idéntica.
- Emulación de timing: uniform jitter 17.2%, activity jitter ~71% con cola derecha y variación diurna, backoff exponencial hasta 300s. PCAP sintético analizado end-to-end (200 paquetes, jitter medido 66.4%).
- Análisis estático Office benigno con oletools portable: sin macros, sin hits YARA.

Conclusión: el flujo de medición es reproducible sin admin. La detección no debe buscar un intervalo único, sino correlacionar proceso, archivo de estado, endpoint y distribución temporal. Para producción se requiere set real amplio y tráfico real en lab aislado.

## 1. Introducción
Las macros de Office y el beaconing periódico siguen siendo vectores clásicos (MITRE ATT&CK T1566.001, T1204.002, T1071.001). Plataformas de simulación como C2-DECT Lite permiten reproducir esas técnicas en lab para medir detección, sin necesidad de malware real.

Este proyecto se planteó desde 0 como investigación defensiva: emular, medir impacto, documentar y crear reglas.

## 2. Alcance y autorización
- Solo sistemas propios, carpeta local `investigacion_c2_dect_lite/`, red localhost.
- Sin creación de payload, sin inyección, sin ocultamiento, sin evasión.
- Sin ejecución de macros, sin ejecución de agent/server real en este host (sin Go).
- Herramientas portables en modo usuario, borrables con la carpeta.

## 3. Metodología
1. **Inventario estático** - lectura de código/docs de la copia local 2.0.0 (ver `03_FASE1...`).
2. **Lab local sin admin** - YARA 4.6.0 portable, Python 3.12.10 embeddable + oletools 0.60.2 + scapy 2.8.0 (ver `09_LAB...`).
3. **Análisis estático Office** - muestra benigna .docx sin macros, oleid/olevba + YARA (RUN-005).
4. **Validación completa** - generación sintética reproducible, YARA, métricas FP/FN, prueba ciega (RUN-006, `tools/validar_completa.py`).
5. **Emulación timing** - réplica de `jitter.go` en Python, PCAP sintético manual, análisis offline (RUN-007, `tools/emular_beaconing.py`).

## 4. Inventario (resumen)
- **Comandos cerrados:** 15 read, 6 write, 4 impact con doble puerta (`AGENT-EXEC` + `-allow-impact`).
- **Transporte:** ECDH P-256 + HKDF-SHA256 + AES-256-GCM, `kdfInfo="c2-dect-lite v1 aes"`, rotación cada 200 beacons.
- **Endpoints:** `/agent/checkin`, `/agent/task/result`, `/api/sessions`, `/api/audit/verify`, `/api/scripts/pubkey`, URIs malleables `/api/update`, `/v1/telemetry`.
- **Timing:** base 10s, jitter 30% uniform/activity, backoff exponencial techo 5 min, timeout 20s, watchdog 90s.
- **Scripting:** Lua sandbox sin shell/`os`/`io`, API `c2.*` solo lectura, firmado Ed25519.
- **Estado en disco:** `~/.c2-dect-lite/agent.json` (0600), SQLite server, DPAPI en consola.
- **Limitaciones del framework:** sin TLS en server Lite, sin CI/tests, consola Windows-only.

## 5. Resultados

### 5.1 Análisis estático Office
Muestra `benigno_limpio.docx` (SHA256 AC072A...):
- oleid: Word 2007+ OpenXML, VBA Macros **No**, XLM No, relaciones externas 0.
- olevba: `No VBA or XLM macros found.`
- YARA: sin hits.

### 5.2 Validación YARA (piloto sintético)
- Limpio n=33, positivo simulado n=12, prueba ciega anonimizada.
- **TP 12/12, TN 33/33, FP 0, FN 0, precisión 1.0, recall 1.0.**
- Ajuste v1.1: regla Lua de 3 a 2 strings (ejemplo mínimo solo tiene 2).
- Detalle: `validacion_completa/resultados_detalle.csv`

### 5.3 Emulación beaconing
| Escenario | Media | Jitter |
|---|---|---|
| uniform 10s 30% | 10.00s | 17.2% |
| activity 10s | 16.85s | 71.0% |
| none fijo | 10.00s | 0% |
PCAP sintético 200 pkts: media 13.22s, jitter medido 66.4%, tamaño 43B constante.

### 5.4 Impacto (matriz resumida)
- Server comprometido: JWT robado permite impersonar operador; sin TLS metadatos visibles; auditoría hash-chain detecta manipulación.
- Agent detectado: proceso + `agent.json` + beacon periódico + `/agent/checkin` es correlación fiable.
- Impacto por defecto bajo-medio por diseño (solo read/write sin gate).

## 6. Detecciones entregadas
- `reglas.yar` v1.1: 4 reglas (Agent_Artifact, Malleable_URIs, Lua_Script, Office_Macro_Generica)
- `sigma_beaconing_periodico.yml`: plantilla por conteo en ventana para WINWORD/EXCEL/agent → 8443
- `analizar_pcap_beacon.py`: estadísticas de periodicidad offline con scapy portable
- `validar_yara.ps1` + `tools/validar_completa.py`: reproducibilidad

## 7. Recomendaciones defensivas
1. Bloquear macros desde internet (MOTW), Vista protegida, ASR para Office.
2. No buscar intervalo único: buscar distribución, cambio diurno, destino único y tamaño constante.
3. Correlacionar YARA (archivo) + Sigma/Zeek/Suricata (red) + inventario de proceso/archivo.
4. Custodiar secretos tipo `C2_JWT_SECRET`, rotar, no exponer server sin TLS.
5. Medir en lab antes de desplegar reglas en producción.

## 8. Limitaciones
- Set limpio sintético, no macros reales de empresas. Set positivo simulado en texto/Lua, no binarios/macros ejecutables.
- Emulación matemática de timing, no tráfico real del agent (sin Go en host).
- Sin VM, sin Sysmon/Npcap por falta de admin: se usaron logs y PCAP offline.
- n pequeño para producción. Ampliar a 100+ y datasets públicos antes de uso en SOC.

## 9. Reproducibilidad (sin admin)
```powershell
# YARA portable
.\tools\YARA\yara64.exe .\reglas.yar .\ruta\archivo

# oletools portable
.\tools\PythonPortable\python.exe -m oletools.oleid .\muestra.docx
.\tools\PythonPortable\python.exe -m oletools.olevba .\muestra.docx

# Validación completa (regenera sets y mide)
.\tools\PythonPortable\python.exe .\tools\validar_completa.py

# Emulación timing + PCAP sintético
.\tools\PythonPortable\python.exe .\tools\emular_beaconing.py
.\tools\PythonPortable\python.exe .\analizar_pcap_beacon.py .\fase2_emulacion_localhost\beacon_sintetico_activity_10s.pcap --ip 127.0.0.1 --port 8443
```

## 10. Conclusión
Se completó el ciclo desde 0: inventario, lab portable sin admin, análisis estático, validación medida y emulación de timing, con reglas YARA derivadas de evidencia. Es publicable como informe técnico defensivo con las limitaciones declaradas. El siguiente paso para uso en producción es set real amplio y tráfico real en lab aislado.

## Referencias
- C2-DECT Lite 2.0.0 - Nakano-04/c2-dect-lite (README, CHANGELOG, FAQ, docs/SCRIPTING_LITE.md)
- MITRE ATT&CK: T1566.001, T1204.002, T1071.001, T1059
- YARA 4.6.0, oletools 0.60.2, Python 3.12.10, scapy 2.8.0
- Archivos del proyecto: 00-13, reglas.yar, tools/, validacion_completa/, fase2_emulacion_localhost/

---
*Informe generado 2026-11-06. Revisar checklist 11_CHECKLIST_PUBLICACION.md para pendientes de publicación amplia.*

