# Fase 1 - Inventario estático (sin ejecución)
Fuente: `C:\Users\BALDEONSARMIENTOLUIS\Desktop\test\c2-dect-lite-2.0.0`
Fecha: 2026-11-06
Método: lectura de código y docs. No se compiló ni ejecutó agent/server.

## 1. Versión y estructura
- Versión: 2.0.0 (`agent/main.go: Version = "2.0.0"`, CHANGELOG 2.0.0)
- Licencia: Non-Commercial, solo testing autorizado / educación
- Estructura verificada:
  - `agent/` : catalog.go, commands.go, jitter.go, main.go, platform.go, scripting.go, transport.go
  - `server/` : api/, auth/, cmd/, core/, crypto/, db/, marketplace/, profiles/
  - `gui/C2Dect/` : consola WPF (Windows-only)
  - `scripttrust/` : cripto compartida
  - `scripts/` : e2e.ps1, gui_smoke.ps1
  - `docs/SCRIPTING_LITE.md`

## 2. Catálogo de comandos - `agent/catalog.go`
Catálogo cerrado y compartido con `server/api/commands.go`. Comando desconocido se rechaza, no cae a shell.

| Nivel | Comandos | Gate |
|-------|----------|------|
| read (15) | sysinfo, hostname, whoami, uptime, ps, netinfo, services, env, connections, ls, cat, stat, hashfile, find, exit | siempre |
| write (6) | mkdir, upload, download, cp, sleep, script | siempre |
| impact (4) | shell, kill, rm, mv | doble: consentimiento `AGENT-EXEC` en server + `-allow-impact` en agent |

Medición representativa:
- Timeout orden externa: 20s (`agent/commands.go: cmdTimeout`)
- Watchdog tarea: 90s (según README/CHANGELOG)
- Sleep: 1 a 86400s
- Chunk resultados: 256 KiB (`main.go: ChunkSize`)

Alias observados: ps->processes, connections->netstat, ls->dir, cat->type, cp->copy, rm->del, mv->move, find->search

## 3. Transporte y endpoints - `agent/transport.go`, README
- Crypto: ECDH P-256 + HKDF-SHA256 + AES-256-GCM
- `kdfInfo = "c2-dect-lite v1 aes"` <- string estable para YARA
- Rotación cada `C2_KEY_ROTATION_EVERY` (defecto 200, 3 en e2e)
- Re-negociación si server reinicia (hello en claro con pubkey)
- Endpoints agent:
  - `POST /agent/checkin`
  - `POST /agent/task/result`
- Endpoints operador (selección):
  - `POST /api/auth/login|refresh|logout`, `GET /api/me`
  - `GET /api/sessions`, `POST /api/sessions/:id/task`, `GET /api/sessions/:id/tasks`
  - `GET /api/loot`, `GET /api/profiles`, `GET /api/audit`, `GET /api/audit/verify`
  - `GET /api/modules`, `GET /api/commands`
  - `GET /api/scripts/pubkey`, `POST /api/scripts/upload`, `POST /api/scripts/:id/run`
- Perfiles malleables en `server/profiles/malleable.go`:
  - URIs: `/api/update`, `/login`, `/dashboard/data`, `/v1/telemetry`, `/api/v2/events`

## 4. Timing / beaconing - `agent/jitter.go`, `main.go`
Defecto agent: `127.0.0.1:8443`, Sleep 10s, Jitter 30%, modo `activity`
- Modos: `uniform`, `activity` (diurno), `none`
- `activityFactor`: 1.0 en 9-18h, 1.35 / 1.8 / 2.4 en noche, cola derecha pesada 0.35-3.20
- Backoff exponencial ante fallo, techo 5 min
- Expiry opcional `-e`, identidad persistente

## 5. Scripting Lite - `docs/SCRIPTING_LITE.md`, `agent/scripting.go`
- Lua firmado Ed25519, sandbox por denegación: sin `os, io, debug, package, require, loadstring, dofile, loadfile, load, collectgarbage`
- API `c2.*`: log, sleep (máx 120s), args, session_id, script_id, beacon, task, fs.list/read/stat, proc.list, sys.info/env, net.info/conns, crypto.sha256/b64encode/b64decode/rand
- Límites: timeout 30s (máx 5 min), salida 1 MiB, fs.read 256 KiB, sleep 120s por llamada
- Scope declarado: `-- scope: lab-only`
- Impacto sigue gated por `-allow-impact`

## 6. Estado en disco
- `~/.c2-dect-lite/agent.json` (0600, dir 0700) - identidad de sesión sobrevive restart (`agent/main.go: defaultStatePath`)
- `~/.c2-dect-lite/data/` (`agent/platform.go`)
- Server SQLite: `c2-dect-lite.db` por defecto
- Refresh token consola protegido con DPAPI

## 7. Configuración sensible
- `C2_JWT_SECRET` obligatorio (>=32 chars), sin ella el server no arranca
- `C2_LISTEN_ADDR` defecto `127.0.0.1:8443`
- `C2_BOOTSTRAP_USER / C2_BOOTSTRAP_PASSWORD` solo primer arranque
- `C2_SCRIPT_PUBKEY` en agent para verificar scripts firmados
- Sin TLS en server Lite (contenido cifrado, metadatos visibles)

## 8. Harness de medición del propio repo
`scripts/e2e.ps1`: levanta server en `127.0.0.1:18443`, health, login, registro agent, task sysinfo, gate de impacto (rechazo sin consentimiento, éxito con consentimiento), catálogo, marketplace, recipes, script Lua firmado vs no firmado, tenants, bootstrap, audit chain, viewer role, aislamiento cross-tenant. 26 checks, 3/3 verde según CHANGELOG.

## 9. Indicadores derivados para YARA/Sigma
Ver `reglas.yar` actualizado con:
- `c2-dect-lite v1 aes`, `/agent/checkin`, `/agent/task/result`, `.c2-dect-lite`, `agent.json`, `AGENT-EXEC`, `/api/sessions`, `/api/update`, `/v1/telemetry`, `c2.task(`, `c2.fs.read`, `-- scope:`

## Conclusión Fase 1
Inventario completo sin ejecución. Listo para Fase 2 (emulación en lab aislado) y Fase 3 (Office benigna).

