# Maschinelles Lernen auf dem Quantencomputer
## Studienarbeit – DHBW Stuttgart Campus Horb, INF2023

Begleitende Notebooks zur Studienarbeit. Vergleich von Quantum Kernel SVM und VQC
gegen klassische Baselines (SVM/RBF, MLP) auf den Datensätzen Iris und Breast Cancer Wisconsin,
ausgeführt auf AerSimulator (ideal), AerSimulator mit IBM Noise Model (ibm_kingston)
und realer IBM Quantum Hardware.

---

## Inhaltsverzeichnis

1. [Voraussetzungen](#voraussetzungen)
2. [Installation](#installation)
3. [JupyterLab mit qml-Umgebung](#jupyterlab-mit-qml-umgebung)
4. [IBM Quantum API-Token](#ibm-quantum-api-token)
5. [Notebook-Übersicht](#notebook-übersicht)
6. [Ergebnisdateien](#ergebnisdateien)

---

## Voraussetzungen

- [Miniconda](https://docs.conda.io/en/latest/miniconda.html) oder Anaconda
- Python 3.11
- IBM Quantum Account (für Noise Model und Hardware-Notebooks): [quantum.ibm.com](https://quantum.ibm.com)

---

## Installation

### 1. Conda-Umgebung erstellen

```bash
conda create -n qml python=3.11 -y
conda activate qml
```

### 2. Pakete installieren

```bash
pip install qiskit==2.4.1
pip install qiskit-aer==0.17.2
pip install qiskit-ibm-runtime==0.47.0
pip install qiskit-machine-learning==0.9.0
pip install qiskit-algorithms==0.4.0
pip install scikit-learn matplotlib pandas notebook jupyterlab
```

> **Hinweis:** Die Versionen sind exakt wie in den Experimenten verwendet.
> Abweichungen können zu veränderten Ergebnissen oder API-Inkompatibilitäten führen.

### 3. Verzeichnisstruktur

```
Notebooks/
├── Ergebnisse/              # CSV-Ausgaben der Experimente (wird automatisch erstellt)
├── ibm_credentials.json     # IBM API-Token (selbst anlegen, siehe unten)
├── utils.py                 # Hilfsfunktionen (save_result, load_ibm_token)
├── check_consistency.py     # Konsistenzprüfung der Notebooks
├── 01_iris_simulator.ipynb
├── ...
└── 14_bitstring_visualisierung.ipynb
```

Das Verzeichnis `Ergebnisse/` wird beim ersten Ausführen automatisch angelegt,
sofern es noch nicht existiert.

---

## JupyterLab mit qml-Umgebung

Damit die `qml`-Umgebung in JupyterLab als Kernel auswählbar ist, muss sie einmalig
als Kernel registriert werden:

```bash
conda activate qml
pip install ipykernel
python -m ipykernel install --user --name qml --display-name "Python (qml)"
```

Anschließend JupyterLab starten:

```bash
jupyter lab
```

In JupyterLab: oben rechts im Notebook auf den Kernel-Namen klicken →
**"Python (qml)"** auswählen. Alle Notebooks sollten mit diesem Kernel ausgeführt werden.

> **Tipp:** Falls der Kernel nicht erscheint, JupyterLab neu starten.
> Mit `jupyter kernelspec list` lässt sich prüfen ob die Umgebung korrekt registriert ist.

---

## IBM Quantum API-Token

Notebooks, die das IBM Noise Model oder echte Hardware verwenden (02, 03, 04, 06, 07, 09, 12, 13),
laden den API-Token aus einer lokalen JSON-Datei. Diese Datei **nicht** in ein Repository einchecken.

### ibm_credentials.json anlegen

Im Notebook-Verzeichnis eine Datei `ibm_credentials.json` mit folgendem Inhalt anlegen:

```json
{
  "name": "Studienarbeit",
  "description": "IBM Quantum API key",
  "apikey": "<dein-token>"
}
```

Den Token unter [quantum.ibm.com](https://quantum.ibm.com) → Account → API Token abrufen.

---

## Notebook-Übersicht

### Hauptexperimente

| Nr. | Datei | Inhalt |
|-----|-------|--------|
| 01 | `01_iris_simulator.ipynb` | Fairer Vergleich aller vier Modelle (QSVM, VQC, SVM/RBF, MLP) auf Iris mit idealem AerSimulator. Kanonische Datenpipeline für alle Folge-Notebooks. |
| 02 | `02_iris_noise.ipynb` | QSVM und VQC auf Iris mit IBM Noise Model (ibm_kingston). Direkter Vergleich ideal vs. verrauscht. |
| 03 | `03_iris_hardware_qsvm.ipynb` | QSVM auf Iris auf echter IBM Quantum Hardware (ibm_kingston), n_train=30. Optimierte Hyperparameter aus NB 12. |
| 04 | `04_qsvm_rauschrobustheit.ipynb` | Rauschrobustheit des QSVM: ideal vs. IBM Noise Model vs. synthetisches Noise Model. Fehlerraten-Sweep für Iris und Breast Cancer. |
| 05 | `05_breast_cancer_simulator.ipynb` | Fairer Vergleich aller vier Modelle auf Breast Cancer (PCA auf 2 Features) mit idealem AerSimulator. |
| 06 | `06_breast_cancer_noise.ipynb` | QSVM und VQC auf Breast Cancer mit IBM Noise Model. Direkter Vergleich ideal vs. verrauscht. |

### VQC-Experimente

| Nr. | Datei | Inhalt |
|-----|-------|--------|
| 07 | `07_vqc_konvergenz_analyse.ipynb` | VQC-Konvergenzverlauf (Kostenfunktion über Iterationen) für Iris und Breast Cancer: ideal vs. IBM Noise vs. synthetisch. Fehlerraten-Sweep. |
| 08 | `08_vqc_noise_iris.ipynb` | Exploratives VQC-Experiment mit SPSA-Optimizer auf Iris (AerSimulator, ideal). Frühes Experiment, nicht kanonisch. |
| 09 | `09_vqc_hardware.ipynb` | VQC auf Iris und Breast Cancer auf echter IBM Quantum Hardware (ibm_kingston). COBYLA, 100 bzw. 50 Iterationen. |

### Analysen

| Nr. | Datei | Inhalt |
|-----|-------|--------|
| 10 | `10_vqc_hyperparameter_iris.ipynb` | VQC Hyperparameter-Analyse auf Iris: 3 Optimizer (COBYLA, SPSA, ADAM) × 4 Iterationsstufen = 12 Läufe. Ausgabe: `ergebnisse_hyperparam.csv`. |
| 11 | `11_vqc_hyperparameter_bc.ipynb` | VQC Hyperparameter-Analyse auf Breast Cancer, analog zu NB 10. Ausgabe: `ergebnisse_hyperparam_bc.csv`. |
| 12 | `12_qsvm_hardware_parameter_analyse.ipynb` | Systematische QSVM-Parameteranalyse mit IBM Noise Model: Feature Map, Reps, Entanglement, Shots, optimization_level, Trainingsgröße. Ausgabe: `ergebnisse_hardware_analyse.csv`. |
| 13 | `13_vqc_hardware_parameter_analyse.ipynb` | Systematische VQC-Parameteranalyse mit IBM Noise Model: 288 Konfigurationen. Ausgabe: `ergebnisse_vqc_parameter_analyse.csv`. |
| 14 | `14_bitstring_visualisierung.ipynb` | Bitstring-Verteilung eines Bell-Zustands: ideal vs. Noise Model vs. IBM Hardware (ibm_kingston, gespeicherte Ergebnisse). Visualisierung des Rauscheffekts. |

### Hilfsdateien

| Datei | Inhalt |
|-------|--------|
| `utils.py` | `save_result()` zum Schreiben der Ergebnisse in CSV; `load_ibm_token()` zum Laden des API-Tokens aus `ibm_credentials.json`. |
| `check_consistency.py` | Prüft alle Notebooks auf Einhaltung der kanonischen Datenpipeline (Features, Scaler, F1-Metrik, Feature Map, Ansatz, Backend). Aufruf: `python check_consistency.py` |

---

## Ergebnisdateien

Alle Experimente schreiben ihre Ergebnisse in das Unterverzeichnis `Ergebnisse/`:

| Datei | Befüllt von | Inhalt |
|-------|-------------|--------|
| `ergebnisse.csv` | NB 01, 02, 05, 06, 09 | Hauptergebnisse aller Modelle (ideal, noise, hardware VQC) |
| `ergebnisse_hardware.csv` | NB 03 | Hardware-Lauf QSVM auf Iris (ibm_kingston, n_train=30). Erweitertes Schema mit Kernel-Zeit, Circuit-Tiefe, Gate-Count und Qubit-Anzahl. |
| `ergebnisse_best_for_hardware.csv` | - | Beste VQC-Konfigurationen aus Hyperparameter-Analyse (Iris: COBYLA/100, BC: COBYLA/50), ideal und noise. Referenzwerte für Hardware-Vergleich. |
| `ergebnisse_hyperparam.csv` | NB 10 | VQC Hyperparameter-Analyse Iris: 3 Optimizer x 4 Iterationsstufen |
| `ergebnisse_hyperparam_bc.csv` | NB 11 | VQC Hyperparameter-Analyse Breast Cancer: 3 Optimizer x 4 Iterationsstufen |
| `ergebnisse_hardware_analyse.csv` | NB 12 | QSVM Parameteranalyse mit Noise Model: 164 Konfigurationen |
| `ergebnisse_vqc_parameter_analyse.csv` | NB 13 | VQC Parameteranalyse mit Noise Model: 322 Konfigurationen |

---

## Kanonische Datenpipeline

Alle Notebooks verwenden exakt diese Pipeline für Vergleichbarkeit:

```python
# Iris: Features 0 und 2 (sepal length, petal length)
X = data[:, [0, 2]]

# Breast Cancer: PCA auf 2 Komponenten
pca = PCA(n_components=2, random_state=42)

# Train/Test Split
train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

# Skalierung
MinMaxScaler(feature_range=(0, 2 * np.pi))

# F1-Metrik
f1_score(..., average='weighted')   # Iris (3 Klassen)
f1_score(..., average='binary')     # Breast Cancer (2 Klassen)
```