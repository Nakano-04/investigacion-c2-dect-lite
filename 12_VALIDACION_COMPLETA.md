# Validación completa (Punto 1 checklist publicación)
Fecha: 2026-11-06 - RUN-006

## Qué se validó
Reglas YARA v1.1 (`reglas.yar`) con YARA 4.6.0 portable, sin admin, sin ejecutar muestras.

## Sets
- **Limpio (n=33):** 20 docx + 10 xlsx sintéticos legítimos (informes, contabilidad, presupuesto, etc.) + 3 controles negativos parciales (solo "Shell", solo "http", solo "AutoOpen" sin combo).
- **Positivo simulado (n=12):** archivos de texto/Lua NO ejecutables con strings del framework (c2.*, /agent/checkin, AGENT-EXEC, URIs malleables, strings VBA simuladas).

Generador y validador: `tools/validar_completa.py` (reproducible, seed 20261106)
Detalle por archivo: `validacion_completa/resultados_detalle.csv`
Resumen automático: `validacion_completa/RESUMEN_VALIDACION.md`

## Resultados
- TP: 12/12, FN: 0
- TN: 33/33, FP: 0
- Precisión: 1.000, Recall: 1.000, Tasa FP: 0.000

## Prueba ciega
Copias con nombre anonimizado por hash, orden aleatorio:
- TP ciega 12, FN 0, FP 0, TN 33 - idéntico al no ciego.

## Hits por regla (positivo)
- C2_DECT_Lite_Agent_Artifact: lua mínimo, lua fs, lua crypto, lua scope, mixto, agent_strings, agent_api
- C2_DECT_Lite_Lua_Script: lua mínimo, lua fs, lua net, lua crypto (tras ajuste)
- C2_DECT_Lite_Malleable_Profile_URIs: malleable.txt
- Office_Macro_Sospechosa_Generica: 3 archivos VBA strings simuladas
- Limpio: ningún hit en ninguna regla

## Ajuste v1 -> v1.1
C2_DECT_Lite_Lua_Script: de 3 a 2 de 7 strings. Motivo: ejemplo mínimo oficial solo tiene c2.log + c2.task(. Los strings c2.* son específicos del framework, 2 mantiene precisión en este set.

## Interpretación honesta
Perfecto en set sintético controlado es esperado - no es rendimiento en producción.
Para publicar en foro/conferencia falta:
- Set limpio REAL (macros legítimas de empresas, n=100+)
- Datasets públicos positivos o PCAPs reales de lab
- Curva de falsos positivos en tráfico/archivos reales

Este resultado valida el *flujo* y la *precisión inicial*, no un detector listo para SOC.

## Conclusión
Punto 1 del checklist: **completado en modo piloto sintético**.
Siguiente: Fase 2 medición localhost y ampliar set real antes de publicar.

