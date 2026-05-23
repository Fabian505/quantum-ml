"""
check_consistency.py – Konsistenzprüfung aller QML-Notebooks
=============================================================
Prüft ob alle Notebooks die kanonische Pipeline verwenden.
Aufruf: python check_consistency.py
"""

import json
import os
import sys
from pathlib import Path

# ─── Erwartete Werte (kanonische Pipeline) ────────────────────────────────────
EXPECTED = {
    'iris_features':    "data[:, [0, 2]]",
    'bc_pca':           "PCA(n_components=2, random_state=42)",
    'test_size':        "test_size=0.3",
    'random_state':     "random_state=42",
    'stratify':         "stratify=y",
    'scaler':           "MinMaxScaler(feature_range=(0, 2 * np.pi))",
    'f1_iris':          "average='weighted'",
    'f1_bc':            "average='binary'",
    'feature_map_fn':   "zz_feature_map(",          # Funktion, nicht Klasse
    'feature_map_cls':  "ZZFeatureMap(",             # deprecated – sollte NICHT vorkommen
    'ansatz_fn':        "real_amplitudes(",          # Funktion, nicht Klasse
    'ansatz_cls':       "RealAmplitudes(",           # deprecated – sollte NICHT vorkommen
    'fidelity_bug':     "ComputeUncompute(sampler=",
    'fidelity_fix':     "transpiler=pm",
    'noise_backend':    "ibm_kingston",
    'old_backend':      "ibm_marrakesh",             # sollte nicht mehr vorkommen
    'shots':            "default_shots = 1024",
    'opt_level':        "optimization_level=1",
}

# ─── Notebook-Definitionen ────────────────────────────────────────────────────
# Format: (Dateiname, Datensatz, hat_noise_model, hat_pm, hat_hardware)
NOTEBOOKS = [
    ("02_iris_fair.ipynb",                  "iris", False, False, False),
    ("04_breast_cancer_fair.ipynb",         "bc",   False, False, False),
    ("06_vergleich_iris_noise.ipynb",       "iris", True,  True,  False),
    ("07_vergleich_bc_noise.ipynb",         "bc",   True,  True,  False),
    ("12_hardware_parameter_analyse.ipynb", "both", True,  True,  False),
    ("13_vqc_parameter_analyse.ipynb",      "iris", True,  True,  False),
    ("14_hardware_qk_iris.ipynb",           "iris", False, True,  True),
]

# ─── Hilfsfunktionen ─────────────────────────────────────────────────────────

def load_notebook_source(path):
    with open(path) as f:
        nb = json.load(f)
    return '\n'.join(''.join(c['source']) for c in nb['cells'])


def check(src, pattern, expect_present=True, label=None):
    present = pattern in src
    ok = present == expect_present
    status = "✅" if ok else "❌"
    msg = label or pattern[:60]
    if not ok:
        direction = "fehlt" if expect_present else "sollte nicht vorkommen"
        return False, f"  {status} {msg!r} {direction}"
    return True, f"  {status} {msg}"


# ─── Hauptprüfung ─────────────────────────────────────────────────────────────

def check_notebook(nb_file, dataset, has_noise, has_pm, is_hardware, nb_dir="."):
    path = os.path.join(nb_dir, nb_file)
    if not os.path.exists(path):
        print(f"\n⚠️  {nb_file} – nicht gefunden, übersprungen")
        return

    src = load_notebook_source(path)
    errors = []
    results = []

    def run(pattern, expect=True, label=None):
        ok, msg = check(src, pattern, expect, label)
        results.append(msg)
        if not ok:
            errors.append(msg)

    # ── Datenpipeline ──────────────────────────────────────────────────────
    if dataset in ("iris", "both"):
        run("data[:, [0, 2]]",              label="Iris Features [0,2]")
        run("test_size=0.3",                label="test_size=0.3")
        run("random_state=42",              label="random_state=42")
        run("stratify=y",                   label="stratify=y")
        run("MinMaxScaler(feature_range=(0, 2 * np.pi))", label="Scaler [0, 2π]")
        run("average='weighted'",           label="F1 average=weighted (Iris)")

    if dataset in ("bc", "both"):
        run("PCA(n_components=2, random_state=42)", label="BC PCA(2, rs=42)")
        run("average='binary'",             label="F1 average=binary (BC)")

    # ── Feature Map ────────────────────────────────────────────────────────
    run("zz_feature_map(",  expect=True,  label="zz_feature_map() Funktion")
    run("ZZFeatureMap(",    expect=False, label="ZZFeatureMap Klasse (deprecated)")

    # ── Ansatz (nur wenn VQC vorkommt) ────────────────────────────────────
    if "VQC" in src or "vqc" in src:
        run("real_amplitudes(", expect=True,  label="real_amplitudes() Funktion")
        run("RealAmplitudes(",  expect=False, label="RealAmplitudes Klasse (deprecated)")

    # ── Noise Model ────────────────────────────────────────────────────────
    if has_noise:
        run("ibm_kingston",   expect=True,  label="Backend ibm_kingston")
        run("ibm_marrakesh",  expect=False, label="Altes Backend ibm_marrakesh")

        # Wenn ComputeUncompute verwendet wird, muss transpiler=pm dabei sein
        if "ComputeUncompute" in src:
            run("transpiler=pm", expect=True, label="fidelity Bug-Fix: transpiler=pm")

    # ── PassManager ────────────────────────────────────────────────────────
    if has_pm:
        run("generate_preset_pass_manager", label="generate_preset_pass_manager")
        run("optimization_level=1",         label="optimization_level=1")

    # ── Hardware ───────────────────────────────────────────────────────────
    if is_hardware:
        run("SamplerV2",     label="Hardware SamplerV2")
        run("transpiler=pm", label="Hardware: transpiler=pm in fidelity")

    # ── Ausgabe ────────────────────────────────────────────────────────────
    n_err = len(errors)
    status = "✅ OK" if n_err == 0 else f"❌ {n_err} Problem(e)"
    print(f"\n{'─'*60}")
    print(f"  {nb_file}  [{status}]")
    print('─'*60)
    for r in results:
        print(r)

    return n_err


# ─── Entry Point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    nb_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    print("=" * 60)
    print("  QML Notebook Konsistenzprüfung")
    print("=" * 60)

    total_errors = 0
    for nb_file, dataset, has_noise, has_pm, is_hardware in NOTEBOOKS:
        result = check_notebook(nb_file, dataset, has_noise, has_pm, is_hardware, nb_dir)
        if result:
            total_errors += result

    print(f"\n{'='*60}")
    if total_errors == 0:
        print("  ✅ Alle Notebooks konsistent.")
    else:
        print(f"  ❌ {total_errors} Problem(e) gefunden – siehe Details oben.")
    print("=" * 60)
