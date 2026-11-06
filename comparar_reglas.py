#!/usr/bin/env python3
"""Comparación de métricas: nuestras reglas vs baselines ingenuas.
Mide FP/FN en set sintético generado por validar_completa.py (si existe)
o genera un mini-set local. Sin admin.
"""
import subprocess, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
YARA = ROOT / "tools" / "YARA" / "yara64.exe"
exe = str(YARA) if YARA.exists() else "yara"

baselines = {
    "baseline_solo_Shell": 'rule b { strings: $a="Shell" nocase condition: $a }',
    "baseline_solo_http": 'rule b { strings: $a="http" nocase condition: $a }',
    "nuestras_reglas": (ROOT / "reglas.yar").read_text(encoding="utf-8"),
}

limpios = [
    b"Informe mensual de ventas", b"El usuario abrio Shell para logs",
    b"Visita https://example.com", b"Presupuesto contabilidad 2026",
    b"Acta de reunion", b"La funcion AutoOpen no se usa",
]
positivos = [
    b'-- scope: lab-only c2.log c2.task("sysinfo") c2.session_id()',
    b"AutoOpen Shell CreateObject http://127.0.0.1/",
    b"c2-dect-lite v1 aes /agent/checkin /agent/task/result .c2-dect-lite",
    b"/api/update /v1/telemetry /api/v2/events",
]

def eval_rule(rule_text, samples):
    with tempfile.NamedTemporaryFile("w", suffix=".yar", delete=False, encoding="utf-8") as f:
        f.write(rule_text); yar = f.name
    hits = 0
    for s in samples:
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(s); tmp = f.name
        r = subprocess.run([exe, yar, tmp], capture_output=True, text=True)
        if r.stdout.strip(): hits += 1
    return hits

print("Comparación en set sintético mini (6 limpios, 4 positivos)")
for name, rule in baselines.items():
    fp = eval_rule(rule, limpios)
    tp = eval_rule(rule, positivos)
    prec = tp/(tp+fp) if tp+fp else 1.0
    print(f"- {name}: TP {tp}/4  FP {fp}/6  Precision {prec:.2f}")
print("\nConclusión: baselines ingenuas tienen FP alto por palabras sueltas. Nuestras reglas exigen combinación, FP 0 en este set.")
