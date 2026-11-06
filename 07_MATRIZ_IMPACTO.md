# Matriz de impacto — C2-DECT Lite 2.0.0 (medición en lab)

| Escenario | Probabilidad lab | Impacto | Detección esperada | Evidencia |
|-----------|------------------|---------|--------------------|-----------|
| Beaconing normal | Alta | Bajo (solo metadatos sin TLS) | Periodicidad en PCAP | PCAP + analizar_pcap_beacon.py |
| Comando read (sysinfo, ps, netinfo) | Alta | Bajo-Medio (inventario) | Sysmon 1 por tasklist/ipconfig/netstat hijos | Sysmon 1 |
| Comando write (mkdir, cp, upload/download) | Media | Medio (cambio reversible) | Sysmon 11 archivo creado | Sysmon 11 |
| Comando impact sin gate | Baja (bloqueado) | Alto si se salta gate | Error "unknown / without -allow-impact" | Log agent/server |
| Comando impact con doble consentimiento | Baja (solo lab) | Alto | Shell hijo de agent | Sysmon 1 |
| Script Lua firmado | Media | Bajo-Medio (solo lectura) | Red + proceso agent, sin shell | Audit server |
| Script no firmado | Media | Bajo (rechazado) | Error de firma Ed25519 | Audit server |
| Server comprometido (JWT robado) | Baja | Alto (impersonar operador) | Login anómalo, audit chain | /api/audit/verify |
| Agent compromete identidad persistente | Media | Medio (sesión sobrevive reinicio) | Archivo `~/.c2-dect-lite/agent.json` | Sysmon 11 |
| Cross-tenant | Baja | Alto si falla aislamiento | Debería dar 404, no 403 | e2e checks |

## Lectura para el informe
- El diseño Lite es deliberadamente de letalidad baja-media: por defecto solo lee/mueve ficheros.
- El riesgo real en lab no es el agent en sí, sino: falta de TLS, secreto JWT mal custodiado, y persistencia de identidad.
- La detección más fiable no es una sola firma, es correlación: proceso + archivo de estado + beacon periódico + endpoint `/agent/checkin`.
