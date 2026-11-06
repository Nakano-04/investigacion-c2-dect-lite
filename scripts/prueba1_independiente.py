#!/usr/bin/env python3
"""Prueba 1 - Validacion independiente.
Set nuevo con seed distinta (20261107), vocabulario y plantillas
no usadas para desarrollar reglas v1.1. Reglas congeladas, sin reentrenar.
"""
import random, shutil, subprocess
from pathlib import Path

random.seed(20261107)
ROOT = Path(__file__).resolve().parent.parent
_yara_win = ROOT / "tools" / "YARA" / "yara64.exe"
YARA = str(_yara_win) if _yara_win.exists() else (shutil.which("yara") or "yara")
REGLAS = ROOT / "reglas" / "reglas.yar"
BASE = ROOT / "validacion_dinamica" / "independiente"
LIMPIO = BASE / "limpio"; POS = BASE / "positivo"
for d in (LIMPIO, POS): d.mkdir(parents=True, exist_ok=True)
for f in list(LIMPIO.glob("*"))+list(POS.glob("*")): f.unlink()

# Limpio independiente: textos distintos a los de desarrollo
limpio = ["Informe de auditoria externa 2025","Contrato marco servicios","Nomina diciembre","Inventario almacen central","Acta constitutiva","Manual calidad ISO","Propuesta tecnica licitacion","Reporte sostenibilidad","Plan contingencia TI","Encuesta clima laboral","Catalogo repuestos","Guia usuario sistema","Certificado formacion","Minuta comite","Solicitud permiso","Orden trabajo mantenimiento","Balance patrimonial","Flujo caja proyectado","Presentacion directorio","Carta poder notarial"]
for i,t in enumerate(limpio,1):
    (LIMPIO/f"ind_limpio_{i:02d}.txt").write_text(t, encoding="utf-8")

# Positivo independiente: plantillas nuevas no vistas en desarrollo
pos = [
    '-- scope: lab-only\nc2.log(c2.sys.env())\nc2.task("uptime")\n',
    '-- scope: lab-only\nc2.log(c2.net.conns())\nc2.crypto.sha256("z")\n',
    "Workbook_Open CreateObject https://example.org/",
    "Document_Open Shell http://198.51.100.7/",
    "c2-dect-lite v1 aes /agent/task/result AGENT-EXEC",
    "/api/update /v1/telemetry /api/v2/events /dashboard/data",
    '-- scope: lab-only\nc2.beacon()\nc2.fs.list()\n',
    "AutoOpen WScript.Shell http://203.0.113.9/",
    '-- scope: lab-only\nc2.proc.list()\nc2.sys.info()\n',
    "SIMULACION c2.task c2.fs.read c2.session_id -- scope:",
]
for i,t in enumerate(pos,1):
    (POS/f"ind_pos_{i:02d}.txt").write_text(t, encoding="utf-8")

def run(d):
    r=subprocess.run([YARA,"-r",str(REGLAS),str(d)],capture_output=True,text=True)
    return set(l.split(" ",1)[1] if " " in l else l for l in r.stdout.splitlines() if l.strip()), r.stdout

fp,_ = run(LIMPIO); tp,_ = run(POS)
print(f"Prueba 1 independiente (seed 20261107, no usada en desarrollo):")
print(f" Limpio 20 -> FP {len(fp)}  TN {20-len(fp)}")
print(f" Positivo 10 -> TP {len(tp)}  FN {10-len(tp)}")
print(f" Precision {len(tp)/(len(tp)+len(fp)) if len(tp)+len(fp) else 1:.3f} Recall {len(tp)/10:.3f}")
