#!/usr/bin/env python3
"""Prueba 3 - Metricas estadisticas completas.
Precision, Recall, F1, FPR, tiempo de deteccion (scan + beacon).
Usa sets independiente + escala + validacion completa si existen.
"""
import subprocess, shutil, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_yara_win = ROOT / "tools" / "YARA" / "yara64.exe"
YARA = str(_yara_win) if _yara_win.exists() else (shutil.which("yara") or "yara")
REGLAS = str(ROOT/"reglas"/"reglas.yar")

def medir(limpio_dir, pos_dir):
    for d in (limpio_dir, pos_dir):
        if not d.exists(): return None
    t0=time.time()
    r1=subprocess.run([YARA,"-r",REGLAS,str(limpio_dir)],capture_output=True,text=True)
    r2=subprocess.run([YARA,"-r",REGLAS,str(pos_dir)],capture_output=True,text=True)
    dt=time.time()-t0
    fp=len(set(l.split(" ",1)[1] for l in r1.stdout.splitlines() if l.strip()))
    tp=len(set(l.split(" ",1)[1] for l in r2.stdout.splitlines() if l.strip()))
    n_limpio=len(list(limpio_dir.glob("*"))); n_pos=len(list(pos_dir.glob("*")))
    tn=n_limpio-fp; fn=n_pos-tp
    prec=tp/(tp+fp) if tp+fp else 1.0; rec=tp/(tp+fn) if tp+fn else 0
    f1=2*prec*rec/(prec+rec) if prec+rec else 0; fpr=fp/(fp+tn) if fp+tn else 0
    return dict(TP=tp,FN=fn,TN=tn,FP=fp,Precision=round(prec,3),Recall=round(rec,3),F1=round(f1,3),FPR=round(fpr,4),tiempo_s=round(dt,3),n_limpio=n_limpio,n_pos=n_pos)

sets = [
    ("independiente", ROOT/"validacion_dinamica"/"independiente"/"limpio", ROOT/"validacion_dinamica"/"independiente"/"positivo"),
    ("validacion_completa", ROOT/"validacion_dinamica"/"set_limpio", ROOT/"validacion_dinamica"/"set_positivo_simulado"),
    ("escala", ROOT/"escala_dinamica"/"limpio", ROOT/"escala_dinamica"/"positivo"),
]
print("Prueba 3 - Metricas estadisticas:")
for nombre, l, p in sets:
    m=medir(l,p)
    print(f" - {nombre}: {m}")
print("\nTiempo de deteccion beacon (modelo): ver emular_beaconing.py - deteccion por ventana, no por intervalo unico.")
