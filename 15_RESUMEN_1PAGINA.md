# Emulación y detección defensiva de C2-DECT Lite — Resumen 1 página

**2026-11-06 · Lab local sin admin · Informe completo en `14_INFORME_FINAL_PUBLICABLE.md`**

## Qué se hizo
Investigación defensiva desde 0 sobre C2-DECT Lite 2.0.0: inventario estático, análisis Office benigno, validación YARA y emulación de beaconing, todo portable y sin administrador.

## Resultados clave
- **YARA piloto:** 33 limpios / 12 positivos simulados → TP 12/12, TN 33/33, FP 0, FN 0, precisión/recall 1.0. Prueba ciega idéntica.
- **Office benigno:** oleid/olevba sin macros, YARA sin hits.
- **Beaconing:** uniform jitter 17.2% (7-13s), activity jitter 71% (2.5-40s, cola derecha), backoff 10→300s. PCAP sintético 200 pkts analizado: jitter medido 66.4%.

## Detecciones
- `reglas.yar` v1.1 (4 reglas), `sigma_beaconing_periodico.yml`, `analizar_pcap_beacon.py`
- Clave: correlacionar proceso + `~/.c2-dect-lite/agent.json` + `/agent/checkin` + distribución temporal, no un intervalo único.

## Impacto
Por diseño Lite es letalidad baja-media (doble puerta en comandos impact). Riesgo real: secreto JWT, falta de TLS visible en PCAP, persistencia de identidad.

## Recomendaciones
Bloquear macros de internet, Vista protegida, ASR Office, custodiar secretos, medir en lab antes de producción.

## Limitaciones
Set sintético pequeño, emulación matemática (no agent real), sin VM/Sysmon/Npcap. Para producción: set real 100+ y tráfico real en lab aislado.

## Reproducir sin admin
```powershell
.\tools\YARA\yara64.exe .\reglas.yar .\archivo
.\tools\PythonPortable\python.exe -m oletools.oleid .\muestra.docx
.\tools\PythonPortable\python.exe .\tools\validar_completa.py
.\tools\PythonPortable\python.exe .\tools\emular_beaconing.py
```

*Solo lab propio, sin payload real. Framework Non-Commercial de su autor, no redistribuido.*
