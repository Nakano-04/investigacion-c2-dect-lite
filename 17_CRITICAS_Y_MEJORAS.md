# Críticas de la investigación y mejoras aplicadas

Fecha: 2026-11-06
Fuente: revisión externa del proyecto

## Crítica 1 - Entorno localhost: no generaliza a redes reales con EDR, proxies, ruido o tráfico cifrado

**Es válida.** Nuestras mediciones fueron localhost, sin EDR, sin proxy, sin ruido y con PCAP sintético.
El transporte del framework es AES-256-GCM, por lo que en red real el contenido es opaco: solo queda metadata (timing, tamaño, destino).

**Mejoras aplicadas en esta revisión:**
- Simulación de ruido/proxy/TLS en `emular_ruido_proxy_tls.py`: genera PCAP con tráfico benigno mezclado (DNS, HTTP, TLS a otros puertos) + beacon, y mide si el analizador sigue aislando el flujo por IP/puerto.
- Documentado que en producción se requiere Zeek/Suricata con ventana temporal, no solo conteo, y EDR para proceso/archivo.
- Pendiente para admin real: VMs con EDR, proxy HTTP y TLS real (ver `LAB_ADMIN_PLAN.md`).

## Crítica 2 - Sin CI/tests ni empaquetado: estructura plana, dependencias de rutas locales y poca reproducibilidad automatizada

**Es válida.** La estructura a raíz es simple pero sin automatización, y los scripts dependían de rutas portables locales.

**Mejoras aplicadas:**
- CI: `.github/workflows/validacion.yml` - GitHub Actions en Ubuntu que instala YARA, corre `validar_completa.py`, verifica sintaxis YARA y oletools.
- Tests: `test_reglas.py` con unittest - verifica que reglas compilan, que limpio no dispara y que positivo simulado sí.
- Empaquetado: `INSTALACION.md` con dependencias y descarga portable, `run_all.ps1` que descarga YARA/Python portable y corre todo sin admin.
- Rutas: scripts usan `Path(__file__).parent` (raíz del repo), sin rutas absolutas de usuario en código. Las rutas absolutas solo quedan en docs históricos como referencia de fuente.

## Crítica 3 - Sin métricas amplias: faltan tasas FP/FN, comparación con otras reglas y pruebas a escala

**Es válida en parte.** Teníamos FP/FN piloto (33/12, 0 FP/FN) pero sin comparación ni escala.

**Mejoras aplicadas:**
- `comparar_reglas.py`: compara nuestras reglas vs 2 baselines ingenuas (solo "Shell", solo "http") en el mismo set. Muestra FP alto de baselines vs 0 de nuestras reglas por exigir combinación.
- Escala: `validar_completa.py` ampliado a modo escala (200 limpios + 100 positivos sintéticos) con métricas tiempo de escaneo.
- Reporte en `18_METRICAS_AMPLIAS.md` con tablas por regla, precisión/recall y limitaciones de set sintético.

## Conclusión
Las tres críticas se incorporan como limitaciones permanentes del informe v1.0 y como trabajo hecho en v1.1 (CI, tests, ruido, comparación, escala sintética).
Para publicación amplia sigue pendiente: set real 100+, EDR/proxy/TLS reales en VMs, y benchmark contra reglas públicas de YARA-Forge / ET Open.
