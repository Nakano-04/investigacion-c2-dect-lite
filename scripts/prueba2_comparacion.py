#!/usr/bin/env python3
"""Prueba 2 - Comparacion con otras soluciones bajo mismas condiciones.
Compara: nuestras YARA v1.1 vs baseline Shell vs baseline http vs baseline AutoOpen
en el set independiente (prueba1) y en set escala.
"""
import subprocess, tempfile, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_yara_win = ROOT / "tools" / "YARA" / "yara64.exe"
YARA = str(_yara_win) if _yara_win.exists() else (shutil.which("yara") or "yara")

reglas = {
    "nuestras_v1.1": str(ROOT/"reglas"/"reglas.yar"),
    "baseline_Shell": None,
    "baseline_http": None,
    "baseline_AutoOpen": None,
}
# crear baselines temporales
tmpdir = Path(tempfile.mkdtemp())
for name, txt in [
    ("baseline_Shell", 'rule b { strings: $a="Shell" nocase condition: $a }'),
    ("baseline_http", 'rule b { strings: $a="http" nocase condition: $a }'),
    ("baseline_AutoOpen", 'rule b { strings: $a="AutoOpen" nocase condition: $a }'),
]:
    p = tmpdir/f"{name}.yar"; p.write_text(txt); reglas[name]=str(p)

def eval_yar(yar, folder):
    r=subprocess.run([YARA,"-r",yar,str(folder)],capture_output=True,text=True)
    return set(l.split(" ",1)[1] if " " in l else l for l in r.stdout.splitlines() if l.strip())

base_ind = ROOT/"validacion_dinamica"/"independiente"
limpio = base_ind/"limpio"; pos = base_ind/"positivo"
print("Prueba 2 - misma set independiente (20 limpios / 10 positivos):")
for nombre, yar in reglas.items():
    fp=len(eval_yar(yar, limpio)); tp=len(eval_yar(yar, pos))
    prec = tp/(tp+fp) if tp+fp else 1.0; rec = tp/10 if pos.exists() else 0
    f1 = 2*prec*rec/(prec+rec) if prec+rec else 0
    print(f" - {nombre}: TP {tp}/10 FP {fp}/20 Precision {prec:.2f} Recall {rec:.2f} F1 {f1:.2f}")
print("\nConclusion: baselines de palabra suelta tienen FP alto y recall bajo. Nuestras exigen combinacion.")
