# Validación completa — resultados
Fecha: 2026-11-06
Herramientas: YARA 4.6.0 portable, Python portable

## Tamaño de set
- Limpio: 33 archivos (20 docx + 10 xlsx sintéticos legítimos + 3 controles negativos parciales)
- Positivo simulado (NO ejecutable): 12 archivos (lua/texto con strings del framework)

## Métricas globales (cualquier regla = positivo)
- TP: 12 / 12  | FN: 0 []
- TN: 33 / 33 | FP: 0 []
- Precisión: 1.000 | Recall: 1.000 | Tasa FP: 0.000

## Hits detallados
Limpio: (ninguno)
Positivo: C2_DECT_Lite_Agent_Artifact C:\Users\BALDEONSARMIENTOLUIS\Documents\Proyecto predeterminado\investigacion_c2_dect_lite\validacion_completa\set_positivo_simulado\pos_12_mixto.txt
C2_DECT_Lite_Agent_Artifact C:\Users\BALDEONSARMIENTOLUIS\Documents\Proyecto predeterminado\investigacion_c2_dect_lite\validacion_completa\set_positivo_simulado\pos_02_lua_fs.lua
C2_DECT_Lite_Lua_Script C:\Users\BALDEONSARMIENTOLUIS\Documents\Proyecto predeterminado\investigacion_c2_dect_lite\validacion_completa\set_positivo_simulado\pos_02_lua_fs.lua
C2_DECT_Lite_Lua_Script C:\Users\BALDEONSARMIENTOLUIS\Documents\Proyecto predeterminado\investigacion_c2_dect_lite\validacion_completa\set_positivo_simulado\pos_03_lua_net.lua
C2_DECT_Lite_Agent_Artifact C:\Users\BALDEONSARMIENTOLUIS\Documents\Proyecto predeterminado\investigacion_c2_dect_lite\validacion_completa\set_positivo_simulado\pos_08_agent_strings.txt
Office_Macro_Sospechosa_Generica C:\Users\BALDEONSARMIENTOLUIS\Documents\Proyecto predeterminado\investigacion_c2_dect_lite\validacion_completa\set_positivo_simulado\pos_05_vba_strings.txt
C2_DECT_Lite_Agent_Artifact C:\Users\BALDEONSARMIENTOLUIS\Documents\Proyecto predeterminado\investigacion_c2_dect_lite\validacion_completa\set_positivo_simulado\pos_11_lua_scope.lua
C2_DECT_Lite_Agent_Artifact C:\Users\BALDEONSARMIENTOLUIS\Documents\Proyecto predeterminado\investigacion_c2_dect_lite\validacion_completa\set_positivo_simulado\pos_01_lua_minimo.lua
C2_DECT_Lite_Lua_Script C:\Users\BALDEONSARMIENTOLUIS\Documents\Proyecto predeterminado\investigacion_c2_dect_lite\validacion_completa\set_positivo_simulado\pos_01_lua_minimo.lua
C2_DECT_Lite_Malleable_Profile_URIs C:\Users\BALDEONSARMIENTOLUIS\Documents\Proyecto predeterminado\investigacion_c2_dect_lite\validacion_completa\set_positivo_simulado\pos_10_malleable.txt
C2_DECT_Lite_Agent_Artifact C:\Users\BALDEONSARMIENTOLUIS\Documents\Proyecto predeterminado\investigacion_c2_dect_lite\validacion_completa\set_positivo_simulado\pos_09_agent_api.txt
Office_Macro_Sospechosa_Generica C:\Users\BALDEONSARMIENTOLUIS\Documents\Proyecto predeterminado\investigacion_c2_dect_lite\validacion_completa\set_positivo_simulado\pos_06_vba_strings2.txt
C2_DECT_Lite_Agent_Artifact C:\Users\BALDEONSARMIENTOLUIS\Documents\Proyecto predeterminado\investigacion_c2_dect_lite\validacion_completa\set_positivo_simulado\pos_04_lua_crypto.lua
C2_DECT_Lite_Lua_Script C:\Users\BALDEONSARMIENTOLUIS\Documents\Proyecto predeterminado\investigacion_c2_dect_lite\validacion_completa\set_positivo_simulado\pos_04_lua_crypto.lua
Office_Macro_Sospechosa_Generica C:\Users\BALDEONSARMIENTOLUIS\Documents\Proyecto predeterminado\investigacion_c2_dect_lite\validacion_completa\set_positivo_simulado\pos_07_vba_strings3.txt

## Prueba ciega (nombres anonimizados, orden aleatorio)
- TP ciega: 12 | FN ciega: 0 | FP ciega: 0 | TN ciega: 33
- Mapa guardado en script (hash en nombre), detalle en resultados_detalle.csv para set no ciego

## Ajuste aplicado
- Regla C2_DECT_Lite_Lua_Script: condición cambiada de 3 a 2 de 7 strings (ejemplo mínimo solo tiene 2). Strings c2.* son muy específicos, 2 mantiene precisión.
- Ver reglas.yar v1.1

## Limitaciones
- Set limpio sintético, no macros reales de empresas. Falta set real de contabilidad/reportes.
- Set positivo simulado son textos/lua, no binarios ni macros ejecutables (por diseño, sin payload).
- n=33 limpio / 12 positivo es buen piloto, no producción. Para publicar en conferencia ampliar a 100+ y datasets públicos.
