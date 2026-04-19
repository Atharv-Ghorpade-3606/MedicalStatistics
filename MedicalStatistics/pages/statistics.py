import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def disease_distribution():
    st.title("📊 Disease-wise Distribution Analysis")

    # 🔹 LOAD READYMADE CSV (NO UPLOAD)
    df = pd.read_csv("C:\\Users\\Atharv\\OneDrive\\Desktop\\Medical\\MedicalStatistics\\disease_data.csv")

    # Normalize column names
    df.columns = df.columns.str.strip().str.lower()

    # Convert numeric columns safely
    df["age"] = pd.to_numeric(df["age"], errors="coerce")
    df["recovery time"] = pd.to_numeric(df["recovery time"], errors="coerce")
    df.dropna(inplace=True)

    # ---------------- DISEASE DROPDOWN ----------------
    disease = st.selectbox(
        "Select Disease",
        sorted(df["disease"].unique())
    )

    disease_df = df[df["disease"] == disease]

    # ---------------- AGE DISTRIBUTION ----------------
    st.subheader(f"📌 Age Distribution for {disease}")

    fig1, ax1 = plt.subplots()
    ax1.hist(disease_df["age"], bins=10)
    ax1.set_xlabel("Age")
    ax1.set_ylabel("Frequency")
    ax1.set_title(f"Age Distribution ({disease})")

    st.pyplot(fig1)

    # ---------------- RECOVERY TIME DISTRIBUTION ----------------
    st.subheader(f"📌 Recovery Time Distribution for {disease}")

    fig2, ax2 = plt.subplots()
    ax2.hist(disease_df["recovery time"], bins=10)
    ax2.set_xlabel("Recovery Time (days)")
    ax2.set_ylabel("Frequency")
    ax2.set_title(f"Recovery Time Distribution ({disease})")

    st.pyplot(fig2)

    # ---------------- QUICK INSIGHTS ----------------
    st.subheader("📈 Quick Insights")

    col1, col2, col3 = st.columns(3)
    col1.metric("Avg Recovery (days)", f"{disease_df['recovery time'].mean():.1f}")
    col2.metric("Min Age", int(disease_df["age"].min()))
    col3.metric("Max Age", int(disease_df["age"].max()))
