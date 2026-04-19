import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from pathlib import Path

# MAIN PAGE FUNCTION
def show_diagnosis():
    st.title("🩺 Disease Prediction System")
    st.markdown("Predict disease based on selected symptoms.")
    # Load dataset
    
    df = pd.read_csv("C:\\Users\\Atharv\\OneDrive\\Desktop\\Medical\\MedicalStatistics\\pages\\diagnose_data\\dataset.csv")
    # CLEAN DATA (CRITICAL FIX)
    symptom_cols = df.columns[1:]

    df[symptom_cols] = (
        df[symptom_cols]
        .apply(lambda col: col.astype(str).str.strip())
        .replace("", np.nan)
    )
    #Prep all the symptoms    
    all_symptoms = sorted(df[symptom_cols].stack().dropna().unique())
    X = pd.DataFrame(0, index=df.index, columns=all_symptoms)
    for i, row in df.iterrows():
        for symptom in row[symptom_cols].dropna():
            X.at[i, symptom] = 1
    disease_encoder = LabelEncoder()
    y = disease_encoder.fit_transform(df["Disease"])
    #TRAIN MODEL
    X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2, random_state=42)
    model = MultinomialNB()
    model.fit(X_train,y_train)
    accuracy = accuracy_score(y_test, model.predict(X_test))

    #Symptom selection
    st.subheader("🧾 Select Symptoms")
    selected_symptoms = st.multiselect(
        "Choose symptoms you are experiencing:",
        all_symptoms
    )

    def prepare_input(symptoms):
        vec = np.zeros(len(all_symptoms))
        for s in symptoms:
            vec[all_symptoms.index(s)] = 1
        return vec.reshape(1, -1)

    if st.button("🔍 Predict Disease"):
        if not selected_symptoms:
            st.warning("⚠️ Please select at least one symptom.")
        else:
            probs = model.predict_proba(prepare_input(selected_symptoms))[0]#Returns the highest probability which is the first occuring value
            idx = np.argmax(probs)
            disease = disease_encoder.inverse_transform([model.classes_[idx]])[0]
            st.success(f"🧠 **Predicted Disease:** {disease}")
            st.info(f"📊 **Confidence:** {probs[idx] * 100:.2f}%")

    #Diagnostic tests
    st.markdown("---")
    st.subheader("🔬 Diagnostic Tests")
    blood_tab, urine_tab = st.tabs(["🩸 Blood Test", "🧪 Urine Test"])

    #Blood test
    with blood_tab:
        st.subheader("🩸 Blood Composition Analysis")
        blood_volume = st.number_input("Blood Volume (mL)", 2.0, 3.0, 2.5, 0.1)
        plasma = st.number_input("Plasma Volume (mL)", 0.8, blood_volume, 1.4, 0.1)
        rbc = st.number_input("RBC (million / µL)", 4.5) * 1_000_000
        wbc = st.number_input("WBC (cells / µL)", 8000.0)
        platelets = st.number_input("Platelets (cells / µL)", 200000.0)
        def composition(rbc, wbc, p, plasma, total):
            plasma_pct = plasma / total * 100
            rem = 100 - plasma_pct
            total_cells = rbc + wbc + p
            return [
                rbc / total_cells * rem,
                wbc / total_cells * rem,
                p / total_cells * rem,
                plasma_pct
            ]
        healthy = composition(5e6, 7000, 250000, 1.375, 2.5)
        observed = composition(rbc, wbc, platelets, plasma, blood_volume)
        fig, ax = plt.subplots(figsize=(3, 4))
        labels = ["RBCs", "WBCs", "Platelets", "Plasma"]
        colors = ["#ffd11a", "#ff3333", "#ff9933", "#cccccc"]
        def draw(x, vals):
            bottom = 0
            for v, c in zip(vals, colors):
                ax.bar(x, v, bottom=bottom, color=c)
                bottom += v
        draw(0, healthy)
        draw(1, observed)
        ax.set_ylim(0, 100)
        ax.set_xticks([0, 1])
        ax.set_xticklabels(["Healthy", "Observed"])
        ax.legend(labels, fontsize=7)
        st.pyplot(fig)

    #Urine tab
    with urine_tab:
        st.subheader("🧪 Urine Test")
        urine_scale = [
            ("Pale Yellow", "#FFFACD", "Well hydrated", "Normal"),
            ("Yellow", "#FFD700", "Normal urine color", "Healthy"),
            ("Dark Yellow", "#DAA520", "Mild dehydration", "Drink more water"),
            ("Amber", "#FFBF00", "Dehydration", "Dehydration risk"),
            ("Orange", "#FF8C00", "Possible liver issue", "Liver disorder"),
            ("Red", "#B22222", "Blood detected", "UTI / Kidney stones"),
            ("Brown", "#654321", "Severe dehydration", "Liver disorder"),
            ("Cloudy", "#E8E8E8", "Possible infection", "UTI")
        ]
        color_index = st.slider(" ",0,len(urine_scale) - 1,2,label_visibility="collapsed")
        color_name, color_hex, observation, condition = urine_scale[color_index]
        position_percent = (color_index / (len(urine_scale) - 1)) * 100
    #CSS
        st.markdown(
        f"""
        <style>
        /* Remove tooltip number */
        div[data-baseweb="slider"] span {{
            display: none;
        }}
        /* Slider track gradient */
        div[data-baseweb="slider"] > div {{
            background: linear-gradient(
                to right,
                #FFFACD, #FFD700, #DAA520, #FFBF00,
                #FF8C00, #B22222, #654321, #E8E8E8
            );
            height: 12px;
            border-radius: 12px;
        }}
        /* Slider thumb */
        div[data-baseweb="thumb"] {{
            background-color: {color_hex} !important;
            border: 3px solid black;
            width: 22px;
            height: 22px;
        }}
        /* Floating color label */
        .color-label {{
            position: relative;
            top: -40px;
            left: {position_percent}%;
            transform: translateX(-50%);
            font-weight: bold;
            color: {color_hex};
            font-size: 14px;
            background: black;
            padding: 3px 10px;
            border-radius: 10px;
            display: inline-block;
        }}
        </style>
        <div class="color-label">{color_name}</div>
        """,
        unsafe_allow_html=True
        )
        st.divider()
        st.success(f"Observed Color: **{color_name}**")
        st.warning(f"Inference: **{observation}**")
        st.info(f"Possible Condition: **{condition}**")

    #Model Performance
    st.markdown("---")
    st.subheader("📈 Model Performance")
    st.metric("Accuracy", f"{accuracy * 100:.2f}%")
