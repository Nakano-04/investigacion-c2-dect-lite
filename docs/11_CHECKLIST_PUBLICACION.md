# Checklist para publicar - estado 2026-11-06

## Ya hecho
- [x] Plan desde 0, inventario estático Fase 1 grabado
- [x] Herramientas portables sin admin: YARA 4.6.0, Python 3.12.10 + oletools 0.60.2 + scapy 2.8.0
- [x] Análisis estático RUN-005 con muestra benigna: oleid/olevba limpio, YARA 0 FP en n=1
- [x] Reglas YARA v1 (4 reglas), Sigma plantilla, analizador PCAP offline
- [x] Runbooks Fase 2/3 y matriz de impacto
- [x] Run log RUN-001 a RUN-005

## Bloqueante (no publicar sin esto)

### 1. Validación real de detección
- [x] Ampliar set limpio sintético: 33 archivos (20 docx + 10 xlsx + 3 negativos) -> FP 0 (piloto, falta set real 100+)
- [x] Ampliar set positivo simulado: 12 archivos no ejecutables, sin crear malware nuevo
- [x] Medir FN/FP, ajustar regla Lua (3->2 strings, v1.1)
- [x] Ejecutar validación completa con `tools/validar_completa.py` y grabar salida (`12_VALIDACION_COMPLETA.md`)
- [x] Prueba ciega anonimizada: TP 12, TN 33, FP 0, FN 0
- [ ] Pendiente para publicación amplia: set limpio REAL de empresas y datasets públicos positivos

### 2. Emulación medida (Fase 2)
- [x] RUN-007 emulación localhost de timing (modelo jitter.go): uniform 17.2%, activity 71%, backoff medidos
- [x] Análisis PCAP offline con `analizar_pcap_beacon.py` sobre PCAP sintético (200 pkts, jitter 66.4%)
- [x] Resultados grabados en `13_FASE2_EMULACION_RESULTADOS.md` con pipeline end-to-end validado
- [ ] Pendiente tráfico real: ejecutar e2e en lab con Go y re-analizar PCAP real con mismo script

### 3. Informe final publicable
- [x] Resumen ejecutivo, metodología, resultados con tablas, impacto y recomendaciones en `14_INFORME_FINAL_PUBLICABLE.md`
- [x] Limitaciones honestas: sin VM, sin Sysmon, sin Npcap, set sintético pequeño
- [x] Reproducibilidad con comandos exactos y versiones fijadas
- [x] `.gitignore` y `PUBLICACION_README.md` (qué publicar / qué no)
- [ ] Pendiente: revisión por par y prueba de clon limpio en 10 min

### 4. Legal / ética / licencia
- [ ] Declaración: solo lab propio, sin payload real, sin evasión, sin terceros
- [ ] Revisar licencia Non-Commercial de C2-DECT Lite: no redistribuir su código/binarios, solo tu análisis/YARA
- [ ] Verificar que no se publica ningún secreto (.env, JWT, tokens), ni binario del agent, ni muestra ejecutable
- [ ] Licencia de tu publicación (MIT / CC-BY 4.0) y autoría

### 5. Reproducibilidad portable
- [ ] README de raíz con: requisitos (Windows, sin admin), descarga de YARA/Python por link (no subir zip de 10MB+ ni site-packages en git), comandos exactos
- [ ] `.gitignore`: ignorar `tools/PythonPortable/`, `tools/YARA/*.zip`, `lab_artefactos/*.docx` binarios pesados, `*.pcap`
- [ ] Script único `run_all_validacion.ps1` (con Bypass) que corra YARA + oletools y genere reporte
- [ ] Versiones fijadas: YARA 4.6.0, Python 3.12.10, oletools 0.60.2, scapy 2.8.0

## Recomendado (calidad)
- [ ] Revisión por par (otro SOC/estudiante) y correcciones
- [ ] CHANGELOG de reglas YARA, versionado semántico
- [ ] Publicación en GitHub con CI simple (solo lint YARA / markdown)
- [ ] Demo reproducible en 10 min: clonar, descargar portables, correr validación

## No publicar
- Payload, macro ejecutable, binario agent, PCAP con datos reales, credenciales, capturas con IPs/users reales

## Estimación
Con Fase 2 medida + set ampliado + informe final, es publicable como informe técnico / repo de investigación defensiva.
Sin eso, hoy es un buen borrador interno, no una publicación.

