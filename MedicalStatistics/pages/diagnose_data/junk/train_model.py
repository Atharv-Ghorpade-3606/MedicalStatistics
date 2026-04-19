import os
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.calibration import CalibratedClassifierCV

# ---------------- PATHS ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(BASE_DIR, "disease_data.csv")
MODEL_PATH = os.path.join(BASE_DIR, "disease_model.pkl")
SYMPTOMS_PATH = os.path.join(BASE_DIR, "symptoms.pkl")
ENCODER_PATH = os.path.join(BASE_DIR, "label_encoder.pkl")

# ---------------- LOAD DATA ----------------
df = pd.read_csv(DATA_PATH)

# Features & target
X = df.drop("Disease", axis=1)
y = df["Disease"]

# ---------------- LABEL ENCODING ----------------
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# ---------------- RANDOM FOREST ----------------
rf = RandomForestClassifier(
    n_estimators=300,
    max_depth=15,
    min_samples_split=5,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

# ---------------- PROBABILITY CALIBRATION ----------------
model = CalibratedClassifierCV(
    estimator=rf,
    method="sigmoid",
    cv=5
)

# ---------------- TRAIN MODEL ----------------
model.fit(X, y_encoded)

# ---------------- SAVE ARTIFACTS ----------------
with open(MODEL_PATH, "wb") as f:
    pickle.dump(model, f)

with open(SYMPTOMS_PATH, "wb") as f:
    pickle.dump(list(X.columns), f)

with open(ENCODER_PATH, "wb") as f:
    pickle.dump(label_encoder, f)

print("✅ Model, label encoder & symptoms saved successfully")
print("🎯 Diseases learned:", list(label_encoder.classes_))
