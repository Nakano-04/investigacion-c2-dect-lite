# Revisión meta-crítica - forma vs fondo

Fecha: 2026-11-06

## La crítica
"Las limitaciones de fondo persisten. Alcance localhost, sin validación externa, ni CI/tests automatizados, ni métricas FP a escala. La actualización es de forma, no de fondo."

**Es correcta en gran parte.** La v1.1 añadió archivos CI/tests/métricas, pero:
- El CI en GitHub **falló de verdad** (run 42300899047): `FileNotFoundError: tools/YARA/yara64.exe` en Ubuntu. El script estaba hardcodeado a Windows. Eso prueba que la "automatización" era formal, no funcional externamente.
- Las métricas eran n=33/12 sintéticas, sin escala ni comparación externa.
- El alcance sigue siendo localhost sin EDR/proxy/TLS reales. Eso no se resolvió con documentos.

## Corrección de fondo aplicada (v1.2)
1. **CI cross-platform real:** `validar_completa.py` ahora detecta YARA portable Windows o `yara` en PATH Linux. Verificable en Actions (infra externa, no localhost).
2. **Tests que pasan en local y deben pasar en CI:** `test_reglas.py` 5/5 OK.
3. **Escala sintética:** `validar_escala.py` - 500 limpios con vocabulario legítimo que incluye Shell/http/AutoOpen sueltos -> FP 0/500 (0.00%). 200 positivos -> TP 200/200, precisión 1.0, tiempo <1s. Sigue siendo sintético, pero es escala, no n=33.
4. **Comparación externa de baselines:** `comparar_reglas.py` - baselines 0.50 vs nuestras 1.00 en mismo set.

## Lo que sigue SIN resolverse (honesto)
- **Localhost no generaliza:** sin VMs admin, sin EDR, sin proxy/TLS reales, sin ruido real de red corporativa. La simulación de ruido es sintética.
- **Sin validación externa independiente:** CI en GitHub es ejecución externa, pero no es revisión por pares ni dataset público externo (CTU, CICIDS, macros reales de empresas).
- **Set sintético ≠ set real:** FP 0 en sintético no garantiza FP 0 en macros legítimas reales de contabilidad con VBA complejo.
- **Sin tráfico real del agent:** emulación de timing + HTTP benigno localhost, no agent/server real compilado.

## Conclusión honesta
v1.1 fue forma. v1.2 corrige fondo en CI cross-platform y escala sintética, y deja constancia verificable en Actions.
El fondo completo (red real, EDR, set real 100+, revisión externa) requiere lab admin con VMs, que queda como trabajo futuro declarado, no como hecho.
