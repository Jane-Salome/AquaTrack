from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import joblib
import os
from hazard_predictor import generate_synthetic_row, rule_based_detector, generate_dataset

app = Flask(__name__)

MODEL_FILE = "hazard_rf_model.joblib"
if not os.path.exists(MODEL_FILE):
    df = generate_dataset(500)
    feature_cols = ["sea_level", "wave_height", "wind_speed", "pressure", "rainfall", "tide_phase"]
    X, y = df[feature_cols], df["label"]
    from sklearn.ensemble import RandomForestClassifier
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X, y)
    joblib.dump(clf, MODEL_FILE)

clf = joblib.load(MODEL_FILE)
feature_cols = ["sea_level", "wave_height", "wind_speed", "pressure", "rainfall", "tide_phase"]

@app.route("/")
def home():
    rows = [generate_synthetic_row() for _ in range(10)]
    df = pd.DataFrame(rows)
    preds = clf.predict(df[feature_cols])
    df["ML Prediction"] = preds
    df["Rule Prediction"] = df.apply(rule_based_detector, axis=1)
    return render_template("dashboard.html", tables=df.to_dict(orient="records"))

@app.route("/predict", methods=["POST"])
def predict():
    data = {col: float(request.form[col]) for col in feature_cols}
    features = np.array([list(data.values())]).reshape(1, -1)
    ml_pred = clf.predict(features)[0]
    rule_pred = rule_based_detector(data)
    return render_template("result.html", data=data, ml_pred=ml_pred, rule_pred=rule_pred)

if __name__ == "__main__":
    app.run(debug=True)
