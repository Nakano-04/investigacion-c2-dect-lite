# Investigación defensiva desde 0 - C2-DECT Lite
## Emulación, medición de impacto y regla YARA

Fecha inicio: 2026-11-06
Alcance: Solo laboratorio propio, red aislada, sin objetivos de terceros.

### 1. Objetivo
Medir si detectamos la cadena de simulación de c2-dect-lite 2.0.0 y artefactos tipo macro de Office, y mejorar la detección con YARA + Sigma. No se crea ni se distribuye una carga útil real.

### 2. Hipótesis
H1: El beaconing periódico con jitter es detectable por periodicidad/tamaño en PCAP.
H2: Los artefactos en disco/red del agent son detectables con YARA por strings estables del framework.
H3: Una macro benigna de Office que intenta red/proceso hijo es detectable por telemetría (Sysmon 1, 11) aunque el contenido sea benigno.

### 3. Fases desde 0

**Fase 0 - Autorización y laboratorio**
- [ ] Autorización escrita del lab
- [ ] 2 VMs: atacante-lab (server) y víctima-lab (agent/Office), red host-only
- [ ] Snapshots limpios antes de cada corrida
- [ ] Sin salida a internet, sin subir muestras a VT
- Ver: `01_CHECKLIST_LABORATORIO.md`

**Fase 1 - Inventario estático (sin ejecutar nada)**
- [ ] Revisar estructura local: `agent/`, `server/`, `gui/C2Dect/`, `scripttrust/`, `scripts/e2e.ps1`, `docs/SCRIPTING_LITE.md`
- [ ] Extraer catálogo de comandos de `agent/catalog.go` (read/write/impact, doble puerta AGENT-EXEC + -allow-impact)
- [ ] Extraer endpoints y transporte de `agent/transport.go` (`/agent/checkin`, `kdfInfo = "c2-dect-lite v1 aes"`)
- [ ] Tomar hashes SHA256 de fuentes/binarios de lab
- Entregable: tabla de indicadores en `02_PLANTILLA_MEDICION.md`

**Fase 2 - Emulación de beaconing**
- [ ] Usar el harness del propio repo `scripts/e2e.ps1` en lab (26 checks: health, login, registro de agent, tasking sysinfo, gate de impacto, auditoría)
- [ ] Capturar PCAP solo de la red host-only
- [ ] Medir: intervalo, jitter, backoff, tamaño de paquetes, rotación de clave
- [ ] No ejecutar comandos `impact` sin doble consentimiento documentado

**Fase 3 - Emulación Office benigna**
- [ ] Muestra benigna que solo escribe marcador en `C:\Temp` y/o contacta listener local
- [ ] Activar Sysmon, Defender, log de macros, Vista protegida
- [ ] Analizar estáticamente con oletools (`oleid`, `olevba`) antes de abrir
- [ ] Detonar en VM víctima, capturar Sysmon 1/11 y PCAP

**Fase 4 - Medición de impacto**
- Completar `02_PLANTILLA_MEDICION.md` por cada corrida
- Impacto si el server simulado se compromise: JWT, SQLite, auditoría, falta de TLS visible en PCAP
- Impacto si el agent es detectado: proceso, archivo de estado `~/.c2-dect-lite/agent.json`, red local

**Fase 5 - YARA + Sigma**
- [ ] Crear reglas desde indicadores observados (no desde evasión)
- [ ] Validar contra benignas, macros legítimas y limpios -> medir falsos positivos
- Ver: `reglas.yar`
- [ ] Complementar con Sigma para beaconing (YARA no detecta conexiones)

**Fase 6 - Documentación final**
- [ ] Informe: resumen, alcance, metodología, cronología, indicadores, gaps, YARA, recomendaciones
- [ ] Anexos: hashes, PCAP recortado, logs Sysmon, salida oletools

### 4. Criterios de éxito
- [ ] Reproducibilidad: misma corrida con mismo snapshot da mismo resultado
- [ ] Detección medida con tiempo y evidencia, no solo "funciona/no funciona"
- [ ] YARA con <5% falsos positivos en set limpio de prueba
- [ ] Informe auditable por un tercero

### 5. Límites
- No se desarrolla payload oculto, ni inyección, ni evasión.
- No se usa contra sistemas de terceros.
- Todo artefacto malicioso-like se destruye al cerrar el lab.

