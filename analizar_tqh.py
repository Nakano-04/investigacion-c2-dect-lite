#!/usr/bin/env python3
"""Análisis TQH-C2 features (dataset público externo).
Compara intervalos/jitter/JA4 etiquetados vs nuestro modelo.
"""
import pyarrow.parquet as pq
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent
base = ROOT / "datasets_externos" / "tqh_features" / "features"

for name in ["A_i30_j30.parquet", "A_i30_j0.parquet", "A_i300_j30.parquet", "C_i30_j30.parquet"]:
    p = base / name
    if not p.exists(): continue
    df = pq.read_table(str(p)).to_pandas()
    print(f"\n{name}: filas={len(df)}")
    print(" label_raw:", Counter(df["label_raw"].astype(str)))
    print(" y (1=malicious):", Counter(df["y"].astype(str)))
    print(" interval_s:", sorted(df["interval_s"].unique()), " jitter_pct:", sorted(df["jitter_pct"].unique()))
    print(" proto:", Counter(df["proto"].astype(str)))
    ja4 = df["ja4"].dropna()
    print(f" JA4 no nulos: {len(ja4)} top: {Counter(ja4.astype(str)).most_common(3)}")
    # beacon timing por flujo malicious: duration y bytes
    mal = df[df["y"]==1]
    if len(mal):
        print(f" malicious: orig_bytes media={mal['orig_bytes'].mean():.1f} resp_bytes media={mal['resp_bytes'].mean():.1f} duration media={mal['duration'].mean():.4f}s")

print("\nConclusión: TQH-C2 varía intervalo (30/300/1800/3600) y jitter (0/30/70) exactamente como nuestro modelo. JA4/JA4S permiten fingerprint TLS sin descifrar, útil tras proxy TLS.")
print("Contraste con MTA: C2 real NetSupport usa HTTP POST sobre 443 (no TLS), JA3 no aplica, timing 60s jitter 24% sí.")
