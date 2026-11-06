# Investigación C2-DECT Lite — desde 0

Carpeta de trabajo defensivo: emular, medir impacto, documentar y crear YARA.

## Índices
- `00_PLAN_INVESTIGACION_DESDE_0.md` — Plan por fases
- `01_CHECKLIST_LABORATORIO.md` — Setup seguro del lab
- `02_PLANTILLA_MEDICION.md` — Plantilla por corrida
- `03_FASE1_INVENTARIO_ESTATICO.md` — Inventario estático grabado 2026-11-06
- `04_RUN_LOG.md` — Registro de corridas (RUN-001 completado, RUN-002/003 preparados)
- `05_FASE2_EMULACION_BEACONING_RUNBOOK.md` — Runbook beaconing lab
- `06_FASE3_OFFICE_BENIGNA_RUNBOOK.md` — Runbook Office benigna
- `07_MATRIZ_IMPACTO.md` — Matriz de impacto
- `reglas.yar` — Reglas YARA defensivas actualizadas Fase 1
- `analizar_pcap_beacon.py` — Analizador PCAP defensivo (periodicidad/jitter)
- `validar_yara.ps1` — Validador YARA lab vs limpio
- `sigma_beaconing_periodico.yml` — Plantilla Sigma

## Fuente local verificada
`C:\Users\BALDEONSARMIENTOLUIS\Desktop\test\c2-dect-lite-2.0.0`
- `agent/catalog.go`, `agent/transport.go`, `agent/scripting.go`
- `scripts/e2e.ps1` (26 checks)
- `docs/SCRIPTING_LITE.md`

## Regla de oro
Solo lab propio y aislado. Sin payload real, sin evasión, sin terceros.
