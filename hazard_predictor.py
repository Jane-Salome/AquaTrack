# hazard_predictor.py
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

def generate_synthetic_row():
    sea_level = np.random.normal(0.5, 0.1)
    wave_height = np.random.normal(0.5, 0.15)
    wind_speed = np.random.normal(5.0, 2.0)
    pressure = np.random.normal(1013, 4)
    rainfall = max(0.0, np.random.normal(0.0, 1.0))
    tide_phase = np.random.uniform(0, 1)

    label = "normal"
    if np.random.rand() < 0.05:
        sea_level += 2.0
        wave_height += 3.0
        label = "tsunami"
    elif np.random.rand() < 0.15:
        wind_speed += 20
        pressure -= 20
        rainfall += 30
        label = "storm"
    elif np.random.rand() < 0.25:
        tide_phase = 0.5
        sea_level += 1.0
        label = "high_tide"

    return {
        "sea_level": sea_level,
        "wave_height": wave_height,
        "wind_speed": wind_speed,
        "pressure": pressure,
        "rainfall": rainfall,
        "tide_phase": tide_phase,
        "label": label
    }

def generate_dataset(n=500):
    return pd.DataFrame([generate_synthetic_row() for _ in range(n)])

def rule_based_detector(row):
    if row["sea_level"] >= 2.0 or row["wave_height"] >= 3.0:
        return "tsunami"
    if (row["wind_speed"] >= 15) and (row["pressure"] <= 995) and (row["rainfall"] >= 10):
        return "storm"
    if (row["tide_phase"] >= 0.45 and row["tide_phase"] <= 0.6) and (row["sea_level"] >= 0.8):
        return "high_tide"
    return "normal"

if __name__ == "__main__":
    df = generate_dataset(1000)
    feature_cols = ["sea_level", "wave_height", "wind_speed", "pressure", "rainfall", "tide_phase"]
    X, y = df[feature_cols], df["label"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    print(classification_report(y_test, clf.predict(X_test)))
    joblib.dump(clf, "hazard_rf_model.joblib")
