# Fase 3 - Emulación Office benigna (lab aislado)

Objetivo: medir detección de macro Office sin carga útil real.

## Principios
- Muestra benigna: solo escribe marcador en `C:\Temp\prueba.txt` y/o contacta listener local de lab.
- Prohibido: shellcode, inyección, robo de credenciales, persistencia, exfiltración real.
- Análisis estático ANTES de abrir.

## Procedimiento
1. Anotar hash SHA256 de la muestra benigna.
2. Estático: `oleid muestra.docm`, `olevba muestra.docm` -> guardar salida.
3. Pasar por `reglas.yar` con `validar_yara.ps1`.
4. En VM víctima (snapshot limpio): abrir, habilitar macros solo si la hipótesis lo exige, observar.
5. Capturar: Sysmon 1 (proceso hijo de WINWORD/EXCEL), Sysmon 11 (archivo en Temp), PCAP, logs Defender, log de macros Office.
6. Cerrar, exportar evidencia, revertir snapshot.
7. Rellenar `02_PLANTILLA_MEDICION.md`.

## Qué medir
- ¿Office bloqueó por MOTW / Vista protegida?
- ¿Hubo proceso hijo anómalo?
- ¿YARA detectó? ¿Falso positivo?
- Tiempo de detección EDR

## Controles recomendados a probar (documentar si funcionan)
- Macros bloqueadas desde internet
- Vista protegida
- Reglas ASR de Office (bloquear macros en Office, bloquear creación de proceso hijo)
- AppLocker / WDAC para WINWORD.EXE

## Cierre
Muestra destruida tras la corrida. Solo quedan hash, oletools, PCAP y logs en la carpeta de investigación.

