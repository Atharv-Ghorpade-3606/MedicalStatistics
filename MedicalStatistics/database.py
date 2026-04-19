import sqlite3

DB_NAME = "hospital.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def column_exists(cursor, table, column):
    cursor.execute(f"PRAGMA table_info({table})")
    return column in [col[1] for col in cursor.fetchall()]

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # ---------------- PATIENTS ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        gender TEXT,
        status TEXT,
        phone TEXT,
        admission DATE
    )
    """)

    # ---- SAFE COLUMN UPGRADES ----
    upgrades = {
        "blood_group": "TEXT",
        "emergency_contact": "TEXT",
        "address": "TEXT",
        "insurance_policy": "TEXT",
        "coverage_percent": "REAL",
        "last_visited": "DATE"
    }

    for column, dtype in upgrades.items():
        if not column_exists(cursor, "patients", column):
            cursor.execute(f"ALTER TABLE patients ADD COLUMN {column} {dtype}")

    # ---------------- DIAGNOSES ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS diagnoses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        disease TEXT,
        severity TEXT,
        confidence INTEGER,
        date DATE,
        FOREIGN KEY(patient_id) REFERENCES patients(id)
    )
    """)
    upgrades2 = {
        "symptoms": "TEXT",
        "expected_recovery_time": "INTEGER",
        "estimated_cost": "INTEGER"
    }
    for column, dtype in upgrades2.items():
        if not column_exists(cursor, "diagnoses", column):
            cursor.execute(f"ALTER TABLE diagnoses ADD COLUMN {column} {dtype}")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    print("✅ Database initialized and upgraded successfully")