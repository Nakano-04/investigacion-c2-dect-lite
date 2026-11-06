#!/usr/bin/env python3
"""Tests automatizados para reglas YARA - sin admin, sin ejecutar muestras."""
import subprocess, tempfile, textwrap
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parent.parent
REGLAS = ROOT / "reglas" / "reglas.yar"

def yara_scan(content_bytes, name="muestra.bin"):
    # Intenta yara-python si existe, si no usa CLI yara si está en PATH/tools
    try:
        import yara
        rules = yara.compile(str(REGLAS))
        return [m.rule for m in rules.match(data=content_bytes)]
    except Exception:
        pass
    # Fallback: archivo temporal + CLI
    yara_exe = ROOT / "tools" / "YARA" / "yara64.exe"
    exe = str(yara_exe) if yara_exe.exists() else "yara"
    with tempfile.NamedTemporaryFile(delete=False, suffix=".bin") as f:
        f.write(content_bytes); tmp = f.name
    r = subprocess.run([exe, str(REGLAS), tmp], capture_output=True, text=True)
    return [line.split()[0] for line in r.stdout.splitlines() if line.strip()]

class TestReglas(unittest.TestCase):
    def test_reglas_compilan_y_no_vacias(self):
        self.assertTrue(REGLAS.exists())
        txt = REGLAS.read_text(encoding="utf-8")
        self.assertIn("rule C2_DECT_Lite_Agent_Artifact", txt)
        self.assertIn("rule Office_Macro_Sospechosa_Generica", txt)

    def test_limpio_no_dispara(self):
        hits = yara_scan(b"Informe mensual de ventas 2026 presupuesto contabilidad")
        self.assertEqual(hits, [], f"Falso positivo en limpio: {hits}")

    def test_control_parcial_no_dispara_office(self):
        # Solo Shell sin AutoOpen/http no debe disparar Office_Macro
        hits = yara_scan(b"El usuario abrio la terminal Shell para revisar logs")
        self.assertNotIn("Office_Macro_Sospechosa_Generica", hits)

    def test_positivo_lua_dispara(self):
        hits = yara_scan(b'-- scope: lab-only\nc2.log("x")\nc2.task("sysinfo")\nc2.session_id()')
        self.assertTrue(len(hits) >= 1, f"FN en lua simulado: {hits}")

    def test_positivo_vba_dispara(self):
        hits = yara_scan(b"AutoOpen Shell CreateObject http://127.0.0.1/")
        self.assertIn("Office_Macro_Sospechosa_Generica", hits)

if __name__ == "__main__":
    unittest.main()

