# Para publicar este repo - qué incluir y qué no

## Incluir
- 00_*.md a 14_*.md, README.md, PUBLICACION_README.md
- reglas.yar, sigma_beaconing_periodico.yml
- tools/*.py, tools/*.ps1 (scripts defensivos, sin payload)
- validacion_completa/resultados_detalle.csv, RESUMEN_VALIDACION.md
- fase2_emulacion_localhost/RESULTADOS_FASE2.md (no el PCAP si pesa, o sí si es sintético pequeño)
- .gitignore, LICENSE de este informe (CC-BY 4.0)

## No incluir
- tools/PythonPortable/ (binarios, descargar por link en README)
- tools/YARA/*.zip, tools/VirtualBoxPortable/*.exe
- Código/binarios de C2-DECT Lite (licencia Non-Commercial de su autor)
- Secretos: .env, JWT, tokens, agent.json, *.db
- Muestras ejecutables reales (solo benignas/simuladas no ejecutables de este proyecto)

## Licencia sugerida
- Informe y reglas propias: CC-BY 4.0 o MIT
- Referencias al framework: citar autor y licencia original, sin redistribuir

## Antes de publicar
- [ ] Revisar que ningún archivo contiene credenciales reales
- [ ] Probar clon limpio + descarga portables + validación en 10 min
- [ ] Revisión por par

