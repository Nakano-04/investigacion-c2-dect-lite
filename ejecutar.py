#!/usr/bin/env python3
"""Script principal raiz - ejecuta toda la investigacion sin admin.
Uso: py ejecutar.py  o  INICIO.bat
Genera RESUMEN_EJECUCION.md dinamico en la raiz.
"""
import subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PY = sys.executable

pasos = [
    ("Tests YARA", [PY, "-m", "unittest", "test_reglas", "-v"]),
    ("Validacion completa", [PY, "validar_completa.py"]),
    ("Validacion escala 500/200", [PY, "validar_escala.py"]),
    ("Comparacion baselines", [PY, "comparar_reglas.py"]),
    ("Emulacion timing", [PY, "emular_beaconing.py"]),
    ("Ruido/proxy/TLS", [PY, "emular_ruido_proxy_tls.py"]),
]

print("=== Investigacion C2-DECT Lite - ejecucion raiz ===")
resultados = []
for nombre, cmd in pasos:
    print(f"\n--- {nombre} ---")
    r = subprocess.run(cmd, cwd=str(ROOT))
    resultados.append((nombre, r.returncode))
    print(f"[{nombre}] codigo={r.returncode}")

ok = all(c==0 for _,c in resultados)
resumen = "# Resumen de ejecucion raiz\nFecha: ejecucion local sin admin\n\n"
for n,c in resultados:
    resumen += f"- {n}: {'OK' if c==0 else 'FALLO '+str(c)}\n"
resumen += "\nVer 12_VALIDACION_COMPLETA.md, 13_FASE2_EMULACION_RESULTADOS.md, 18_METRICAS_AMPLIAS.md, 21_VALIDEZ_EXTERNA.md\n"
(ROOT/"RESUMEN_EJECUCION.md").write_text(resumen, encoding="utf-8")
print("\nResumen guardado en RESUMEN_EJECUCION.md")
sys.exit(0 if ok else 1)
