from database import get_connection

def save_diagnosis(
    patient_id,
    disease,
    severity,
    confidence,
    symptoms,
    expected_recovery_time,
    estimated_cost
):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO diagnoses (
            patient_id,
            disease,
            severity,
            confidence,
            symptoms,
            expected_recovery_time,
            estimated_cost,
            date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, DATE('now'))""", 
        (patient_id,
        disease,
        severity,
        confidence,
        ", ".join(symptoms),
        expected_recovery_time,
        estimated_cost
    ))
    conn.commit()
    conn.close()
