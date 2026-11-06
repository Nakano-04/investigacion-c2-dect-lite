# Fase 3 — Análisis estático: resultados (RUN-005)
Fecha: 2026-11-06
Modo: local sin admin, herramientas portables

## Muestras analizadas en `lab_artefactos/`
| Archivo | SHA256 | Tipo |
|---------|--------|------|
| benigno_limpio.docx | AC072A82D5C07BF7DD8841DABC550E4CFA7C9256F318BEA67B722EBBE15D99A2 | .docx limpio generado local, sin macros |
| ejemplo_lua_benigno.lua | 5DD31EB927CB0A7C070770E1CB8D54907A7BF39A9672C0F01996E068518A007A | Lua ejemplo público de docs/SCRIPTING_LITE.md, solo lectura |
| simulacion_vba_strings.txt | 62D9BFF80BB1CEF22A4377E3FD8CF9512AADC79D8505475478403099DCD94BE2 | Texto de simulación con strings, NO ejecutable |

Generador benigno: `tools/generar_muestra_benigna.py` (zip OOXML mínimo, sin VBA)

## Oletools (portable Python 3.12.10 + oletools 0.60.2)

### oleid benigno_limpio.docx
- File format: MS Word 2007+ Document (.docx)
- Container: OpenXML
- Encrypted: False
- VBA Macros: **No**
- XLM Macros: No
- External Relationships: 0

### olevba benigno_limpio.docx
- `No VBA or XLM macros found.`
- Conclusión: limpio, sin macros, sin indicadores VBA. Esperado.

## YARA portable 4.6.0 (`tools/YARA/yara64.exe`, `reglas.yar`)

### benigno_limpio.docx
- Sin hits. Correcto (negativo esperado).

### lab_artefactos/ recursivo
```
C2_DECT_Lite_Agent_Artifact  ejemplo_lua_benigno.lua
Office_Macro_Sospechosa_Generica  simulacion_vba_strings.txt
```
- Lua benigno detectado por `c2.task`, `c2.session_id`, `-- scope:` -> regla Agent_Artifact OK.
- Texto de simulación detectado por regla Office_Macro -> OK para strings AutoOpen/Shell/CreateObject/http.
- Nota: `C2_DECT_Lite_Lua_Script` no disparó en ejemplo mínimo (necesita 3 de 7 strings, ejemplo tiene 2). Sugerencia: bajar a 2 o añadir `c2.log` ya cuenta — revisar en validación FPR.

### set_limpio/ (copia de benigno_limpio.docx)
- Sin hits. **0 falsos positivos en set limpio de prueba (n=1).**

## Conclusión Fase 3 estática
- Flujo portable sin admin funciona end-to-end.
- YARA distingue limpio vs artefacto framework / strings VBA en esta prueba controlada.
- Falta: ampliar set limpio (macros legítimas de contabilidad, etc.) y set positivo con PCAPs/datasets públicos antes de producción.
- No se ejecutó ninguna macro. No se creó payload real.

## Próximo paso
Fase 2 localhost: medir beaconing local con logs de server/agent (sin Npcap) o análisis PCAP offline cuando se capture en lab.
