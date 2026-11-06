#!/usr/bin/env python3
"""Prueba a escala sintética: 500 limpios con vocabulario legitimo
que incluye palabras sueltas Shell/http/AutoOpen, y 200 positivos simulados.
Mide FP/FN a escala. Sin admin, sin ejecutar muestras.
"""
import random, shutil, subprocess, time, zipfile
from pathlib import Path

random.seed(20261106)
ROOT = Path(__file__).resolve().parent
_yara_win = ROOT / "tools" / "YARA" / "yara64.exe"
YARA = str(_yara_win) if _yara_win.exists() else (shutil.which("yara") or "yara")
REGLAS = ROOT / "reglas.yar"
BASE = ROOT / "escala_dinamica"
LIMPIO = BASE / "limpio"; POS = BASE / "positivo"
for d in (LIMPIO, POS): d.mkdir(parents=True, exist_ok=True)
for f in list(LIMPIO.glob("*"))+list(POS.glob("*")): f.unlink()

vocab = ["informe","ventas","presupuesto","contabilidad","reunion","contrato","Shell","http","AutoOpen","proyecto","cliente","factura","stock","nomina","manual"]
def txt_legitimo():
    return " ".join(random.choice(vocab) for _ in range(20))

def make_docx(path, text):
    ct='<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>'
    rels='<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>'
    doc=f'<?xml version="1.0"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body><w:p><w:r><w:t>{text}</w:t></w:r></w:p></w:body></w:document>'
    with zipfile.ZipFile(path,"w",zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml",ct); z.writestr("_rels/.rels",rels); z.writestr("word/document.xml",doc)

for i in range(500):
    make_docx(LIMPIO/f"l_{i:04d}.docx", txt_legitimo())
templates = [
    '-- scope: lab-only\nc2.log(c2.session_id())\nc2.task("sysinfo")\n',
    "AutoOpen Shell CreateObject http://127.0.0.1/",
    "c2-dect-lite v1 aes /agent/checkin .c2-dect-lite",
    "/api/update /v1/telemetry /api/v2/events",
]
for i in range(200):
    (POS/f"p_{i:04d}.txt").write_text(random.choice(templates), encoding="utf-8")

def run(d):
    t0=time.time()
    r=subprocess.run([YARA,"-r",str(REGLAS),str(d)],capture_output=True,text=True)
    dt=time.time()-t0
    hits=[l.split()[0] for l in r.stdout.splitlines() if l.strip()]
    return hits, dt, r.stderr

fp_hits, t_limpio, err1 = run(LIMPIO)
tp_hits, t_pos, err2 = run(POS)
# Contar archivos con hit (sin duplicar por regla)
def archivos_con_hit(d):
    r=subprocess.run([YARA,"-r",str(REGLAS),str(d)],capture_output=True,text=True)
    return set(l.split(" ",1)[1] if " " in l else l for l in r.stdout.splitlines() if l.strip())
fp_files=len(archivos_con_hit(LIMPIO)); tp_files=len(archivos_con_hit(POS))
print(f"Escala: limpio 500 -> FP archivos {fp_files} ({fp_files/500*100:.2f}%) en {t_limpio:.1f}s")
print(f"Escala: positivo 200 -> TP archivos {tp_files} ({tp_files/200*100:.1f}%) en {t_pos:.1f}s")
print(f"Precisión escala: {tp_files/(tp_files+fp_files) if tp_files+fp_files else 1:.3f}")
if err1.strip(): print("stderr limpio:",err1[:500])
if err2.strip(): print("stderr pos:",err2[:500])
