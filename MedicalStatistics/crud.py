import pandas as pd
from database import get_connection

# ---------------- PATIENTS ----------------
def add_patient(data):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO patients (
            name, age, gender, blood_group,
            phone, emergency_contact, address,
            insurance_policy, coverage_percent,
            status, admission, last_visited
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["name"],
        data["age"],
        data["gender"],
        data["blood_group"],
        data["phone"],
        data["emergency_contact"],
        data["address"],
        data["insurance_policy"],
        data["coverage_percent"],
        data["status"],
        data["admission"],
        data["last_visited"]
    ))

    conn.commit()
    conn.close()


def update_patient(patient_id, data):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE patients SET
            name = ?, age = ?, gender = ?, blood_group = ?,
            phone = ?, emergency_contact = ?, address = ?,
            insurance_policy = ?, coverage_percent = ?,
            status = ?, last_visited = ?
        WHERE id = ?
    """, (
        data["name"],
        data["age"],
        data["gender"],
        data["blood_group"],
        data["phone"],
        data["emergency_contact"],
        data["address"],
        data["insurance_policy"],
        data["coverage_percent"],
        data["status"],
        data["last_visited"],
        patient_id
    ))

    conn.commit()
    conn.close()


def get_patients():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM patients ORDER BY id DESC", conn)
    conn.close()
    return df
