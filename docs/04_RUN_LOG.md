# Run Log - registro de corridas

## RUN-001 - Fase 1 Inventario estático
- Fecha: 2026-11-06
- Tipo: estático, sin ejecución
- Fuente: `Desktop\test\c2-dect-lite-2.0.0`
- Acciones: lectura de README, CHANGELOG, FAQ, agent/catalog.go, commands.go, jitter.go, main.go, transport.go, scripting.go, docs/SCRIPTING_LITE.md, grep endpoints/config
- Resultado: inventario grabado en `03_FASE1_INVENTARIO_ESTATICO.md`, YARA actualizada
- Estado: completado. Pendiente Fase 2 en lab aislado (requiere VMs con snapshot, no ejecutar en host principal)

## RUN-002 - Preparación Fase 2 (emulación beaconing)
- Fecha: 2026-11-06
- Tipo: preparación documental, sin ejecución en host principal
- Entregables: `05_FASE2_EMULACION_BEACONING_RUNBOOK.md`, `analizar_pcap_beacon.py`, `sigma_beaconing_periodico.yml`, `07_MATRIZ_IMPACTO.md`
- Estado: listo para ejecutar en lab aislado (2 VMs host-only)

## RUN-004 - Pivot a lab local sin admin (2026-11-06)
- Decisión usuario: todo local sin admin, se descarta VirtualBox (requiere drivers/admin)
- Instalado portable sin admin: YARA 4.6.0 (`tools/YARA/yara64.exe` verificado), Python 3.12.10 embeddable (`tools/PythonPortable/python.exe` verificado), oletools 0.60.2 + scapy 2.8.0 en `Lib/site-packages`
- Grabado: `09_LAB_LOCAL_SIN_ADMIN.md`, `tools/run_portable.ps1`
- Estado: herramientas listas para análisis estático, YARA y PCAP offline sin admin

## RUN-005 - Fase 3 análisis estático ejecutado (2026-11-06)
- Muestras: benigno_limpio.docx (AC072A...), ejemplo_lua_benigno.lua (5DD31E...), simulacion_vba_strings.txt (62D9BF...)
- oleid/olevba: benigno sin macros, limpio
- YARA 4.6.0 portable: benigno sin hits, lua detectado por Agent_Artifact, simulación detectada por Office_Macro, set_limpio 0 FP
- Resultados grabados en `10_FASE3_ANALISIS_ESTATICO_RESULTADOS.md`
- Estado: completado sin admin, sin ejecución de macros

## RUN-006 - Validación completa Punto 1 (2026-11-06)
- Script: `tools/validar_completa.py`, YARA 4.6.0 portable, reglas v1.1 (Lua 3->2)
- Set limpio n=33 (20 docx + 10 xlsx + 3 negativos parciales), positivo simulado n=12
- Resultados: TP 12/12, TN 33/33, FP 0, FN 0, Precisión 1.0, Recall 1.0
- Prueba ciega anonimizada: TP 12, TN 33, FP 0, FN 0
- Grabado: `12_VALIDACION_COMPLETA.md`, `validacion_completa/resultados_detalle.csv`, `validacion_completa/RESUMEN_VALIDACION.md`
- Limitación anotada: set sintético, falta set real 100+ para producción/publicación amplia

## RUN-007 - Fase 2 emulación localhost timing (2026-11-06)
- Método: réplica Python de agent/jitter.go, sin ejecutar agent real (sin Go/admin)
- Script: `tools/emular_beaconing.py`, PCAP sintético manual 200 pkts 127.0.0.1:8443
- Resultados: uniform jitter 17.2%, activity jitter 71%, none 0%, backoff 10-300s
- Análisis PCAP: media 13.22s, SD 8.77s, jitter 66.4%, tamaño 43B constante
- Grabado: `13_FASE2_EMULACION_RESULTADOS.md`, `fase2_emulacion_localhost/RESULTADOS_FASE2.md` + PCAP
- Estado: completado en modo modelo. Tráfico real queda pendiente en lab con Go.

## RUN-008 - Informe final publicable (2026-11-06)
- Creado `14_INFORME_FINAL_PUBLICABLE.md` (resumen, metodología, resultados, YARA, impacto, recomendaciones, limitaciones, reproducibilidad)
- Creado `.gitignore` y `PUBLICACION_README.md` (qué publicar / qué no, licencias)
- Estado: informe listo para publicación técnica defensiva con limitaciones declaradas

## RUN-009 - Medición REAL localhost (2026-11-06)
- Ejecutado de verdad: servidor HTTP 127.0.0.1:18080 + cliente 20 peticiones reales, base 2s activity
- Resultados: 20/20 HTTP 200, intervalo medio 2.03s, SD 1.90s, jitter 93.9%, RTT 0-33ms
- CSV: `fase2_emulacion_localhost/medicion_real_localhost.csv`, script `tools/medicion_localhost_real.py`
- Grabado: `16_MEDICION_REAL_LOCALHOST.md`
- Instalador VirtualBox localizado: `Temp\WinGet\Oracle.VirtualBox.7.2.22\VirtualBox-7.2.22-175245-Win.exe` - pendiente ejecución manual como admin por el usuario

## RUN-003 - Preparación Fase 3 (Office benigna)
- Fecha: 2026-11-06
- Entregables: `06_FASE3_OFFICE_BENIGNA_RUNBOOK.md`, `validar_yara.ps1`
- Estado: listo para ejecutar en VM víctima con snapshot. No crear payload real.

