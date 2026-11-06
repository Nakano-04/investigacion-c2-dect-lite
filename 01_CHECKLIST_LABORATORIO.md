# Checklist de laboratorio aislado

## Red y VMs
- [ ] Red host-only / VLAN aislada, sin NAT a internet
- [ ] VM atacante-lab: solo server de simulación
- [ ] VM víctima-lab: solo agent / Office benigno
- [ ] Snapshot limpio numerado: `lab-base-001`
- [ ] Relojes sincronizados entre VMs para timeline

## Telemetría en víctima
- [ ] Sysmon instalado (config SwiftOnSecurity o similar)
- [ ] Defender en modo auditoría primero, luego bloqueo
- [ ] Registro de PowerShell, Office Trust Center
- [ ] Wireshark / tcpdump solo en interfaz host-only

## Herramientas estáticas
- [ ] oletools: `oleid`, `olevba`
- [ ] YARA / YARA-X
- [ ] Hash: `Get-FileHash -Algorithm SHA256`
- [ ] sigma-cli (opcional)

## Antes de cada corrida
- [ ] Snapshot tomado
- [ ] PCAP vacío / listo
- [ ] Hora de inicio anotada
- [ ] Hipótesis de la corrida anotada

## Después de cada corrida
- [ ] Exportar PCAP, logs Sysmon, salida oletools, hash
- [ ] Completar `02_PLANTILLA_MEDICION.md`
- [ ] Revertir a snapshot
- [ ] Borrar artefactos de la corrida

## Prohibido
- [ ] Enviar el archivo por correo/WhatsApp
- [ ] Subir a VirusTotal u otros servicios online
- [ ] Probar en equipo de trabajo real o de terceros
- [ ] Ejecutar comandos `impact` sin consentimiento explícito documentado
