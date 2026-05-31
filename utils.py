import pandas as pd
import json
import os

CSV_PATH = "Ergebnisse/ergebnisse.csv"


def load_ibm_token(path="ibm_credentials.json"):
    """Lädt den IBM Quantum API-Token aus einer JSON-Datei.

    Erwartet eine Datei mit folgendem Format:
        {
          "apikey": "<token>"
        }

    Args:
        path: Pfad zur JSON-Datei (Standard: ibm_credentials.json im Arbeitsverzeichnis)

    Returns:
        API-Token als String
    """
    with open(path) as f:
        return json.load(f)["apikey"]

def save_result(modell, datensatz, backend, accuracy, f1, trainingszeit, inferenzzeit, **kwargs):
    entry = {
        "Modell": modell,
        "Datensatz": datensatz,
        "Backend": backend,
        "Accuracy": round(accuracy, 4),
        "F1": round(f1, 4),
        "Trainingszeit_s": round(trainingszeit, 4),
        "Inferenzzeit_s": round(inferenzzeit, 4),
    }
    entry.update(kwargs)  # z.B. Feature_Map, Reps, Shots etc.
    
    df = pd.DataFrame([entry])
    if os.path.exists(CSV_PATH):
        df.to_csv(CSV_PATH, mode='a', header=False, index=False)
    else:
        df.to_csv(CSV_PATH, index=False)
    
    print(pd.read_csv(CSV_PATH).to_string(index=False))