import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Disease Prediction System",
    page_icon="🩺",
    layout="wide"
)

st.title("🩺 Disease Prediction System")
st.markdown("Predict disease based on selected symptoms.")

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    return pd.read_csv("dataset.csv")

df = load_data()
df.fillna("None", inplace=True)

symptom_cols = df.columns[1:]

# =========================
# PREPARE SYMPTOMS
# =========================
all_symptoms = sorted(
    set(
        symptom
        for col in symptom_cols
        for symptom in df[col].unique()
        if symptom != "None"
    )
)

# Binary feature matrix
X = pd.DataFrame(0, index=df.index, columns=all_symptoms)

for i, row in df.iterrows():
    for symptom in row[symptom_cols]:
        if symptom != "None":
            X.at[i, symptom] = 1

# Encode disease labels
disease_encoder = LabelEncoder()
y = disease_encoder.fit_transform(df["Disease"])

# =========================
# TRAIN MODEL
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = MultinomialNB()
model.fit(X_train, y_train)

# =========================
# MODEL ACCURACY
# =========================
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# =========================
# SYMPTOM SELECTION (MAIN SCREEN)
# =========================
st.subheader("🧾 Select Symptoms")

selected_symptoms = st.multiselect(
    "Choose symptoms you are experiencing:",
    all_symptoms
)

# =========================
# PREDICTION
# =========================
def prepare_input(symptoms):
    input_data = np.zeros(len(all_symptoms))
    for symptom in symptoms:
        input_data[all_symptoms.index(symptom)] = 1
    return input_data.reshape(1, -1)

if st.button("🔍 Predict Disease"):
    if not selected_symptoms:
        st.warning("⚠️ Please select at least one symptom.")
    else:
        input_data = prepare_input(selected_symptoms)

        # Prediction
        pred_class = model.predict(input_data)[0]
        pred_disease = disease_encoder.inverse_transform([pred_class])[0]

        # Confidence %
        prob = model.predict_proba(input_data)[0][pred_class] * 100

        st.success(f"🧠 **Predicted Disease:** {pred_disease}")
        st.info(f"📊 **Confidence:** {prob:.2f}%")

# =========================
# MODEL PERFORMANCE
# =========================
st.divider()
st.subheader("📈 Model Performance")
st.metric("Accuracy", f"{accuracy * 100:.2f}%")
