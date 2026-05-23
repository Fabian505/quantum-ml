import pandas as pd
import os

CSV_PATH = "Ergebnisse/ergebnisse.csv"

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