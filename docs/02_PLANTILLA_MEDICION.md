# Plantilla de medición - una por corrida

## Corrida
- ID: `RUN-___`
- Fecha/hora inicio-fin:
- Snapshot usado:
- Hipótesis:
- Operador:

## Emulación
- [ ] Beaconing (server+agent lab vía e2e)
- [ ] Office benigna
- [ ] Script Lua Lite firmado (solo lectura)

## Observaciones

| # | Hora | Fuente | Evidencia | ¿Detectado? |
|---|------|--------|-----------|-------------|
| 1 | | PCAP | Intervalo / jitter / tamaño | |
| 2 | | Sysmon 1 | Proceso hijo de WINWORD/EXCEL/agent | |
| 3 | | Sysmon 11 | Archivo creado en Temp / estado agent | |
| 4 | | EDR/Defender | Alerta y tiempo | |
| 5 | | Server Audit | Entrada hash-chain verificada | |

## Impacto medido
- Confidencialidad: ¿Qué datos benignos salieron al listener local?
- Integridad: ¿Qué archivos se crearon/modificaron?
- Disponibilidad: ¿Se colgó algún proceso? (watchdog 90s, timeout 20s)
- Persistencia: ¿Sobrevive a reinicio? (identidad en `~/.c2-dect-lite/agent.json`)
- Detección: Tiempo hasta alerta, gap si no hubo

## Indicadores para YARA
- Hash SHA256 archivo:
- Strings observados (oletools / strings):
- Endpoints observados:
- Falsos positivos en set limpio:

## Conclusión de la corrida

