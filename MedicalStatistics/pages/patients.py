import streamlit as st
from datetime import date
from crud import get_patients, add_patient, update_patient

#ADD PATIENT
@st.dialog("➕ Add New Patient")
def add_patient_dialog():
    with st.form("add_patient_form"):       
    #ROW 1 
       col1, col2, col3 = st.columns([2, 1, 1])
       with col1:
           name = st.text_input("Full Name *", placeholder="Enter patient name")
       with col2:
           age = st.number_input("Age *", min_value=0, max_value=120, step=1)
       with col3:
           gender = st.radio(
            "Gender *",
            ["Male", "Female", "Other"],
            horizontal=True
        )

    # ---------- ROW 2 ----------
       col4, col5 = st.columns(2)
       with col4:
           phone = st.text_input("Phone *", placeholder="+91 98765 43210")
       with col5:
           email = st.text_input("Email", placeholder="patient@email.com")

    # ---------- ROW 3 ----------
       col6, col7 = st.columns([2, 2])
       with col6:
           blood_group = st.radio(
            "Blood Group",
            ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
            horizontal=True
        )
       with col7:
        emergency_contact = st.text_input(
            "Emergency Contact",
            placeholder="Emergency contact number"
        )

    # ---------- ROW 4 ----------
       address = st.text_area("Address", placeholder="Full address")

    # ---------- INSURANCE SECTION ----------
       st.markdown("### Insurance Details")
       col8, col9, col10 = st.columns(3)
       with col8:
           insurance_provider = st.text_input(
            "Provider",
            placeholder="Insurance company"
        )
       with col9:
           insurance_policy = st.text_input(
            "Policy ID",
            placeholder="Policy number"
        )
       with col10:
           coverage_percent = st.number_input(
            "Coverage %",
            min_value=0,
            max_value=100
        )

    # ---------- ROW 6 ----------
       col11, col12 = st.columns(2)
       with col11:
           admission_date = st.date_input("Admission Date")
       with col12:
           status = st.radio(
            "Status",
            ["Active", "Recovered", "Critical", "Discharged"],
            horizontal=True
        )

    # ---------- ACTION BUTTONS ----------
       col_cancel, col_submit = st.columns([3, 1])
       with col_submit:
        submitted = st.form_submit_button("Add Patient")


        if submitted:
            add_patient({
                "name": name,
                "age": age,
                "gender": gender,
                "blood_group": blood_group,
                "phone": phone,
                "emergency_contact": emergency_contact,
                "address": address,
                "insurance_policy": insurance_policy,
                "coverage_percent": coverage_percent,
                "status": status,
                "admission": str(admission_date),
                "last_visited": str(admission_date
                )
            })

            st.success("Patient added successfully")
            st.rerun()



# ---------------- EDIT PATIENT ----------------
@st.dialog("✏️ Edit Patient")
def edit_patient_dialog(patient):

    with st.form("edit_patient_form"):

        col1, col2, col3 = st.columns(3)
        with col1:
            name = st.text_input("Name", patient["name"])
        with col2:
            age = st.number_input("Age", 0, 120, patient["age"])
        with col3:
            gender = st.radio(
                "Gender",
                ["Male", "Female", "Other"],
                index=["Male", "Female", "Other"].index(patient["gender"]),
                horizontal=True
            )

        phone = st.text_input("Phone", patient["phone"])
        emergency_contact = st.text_input("Emergency Contact", patient["emergency_contact"])
        address = st.text_area("Address", patient["address"])
        insurance_policy = st.text_input("Insurance Policy", patient["insurance_policy"])
        status = st.selectbox(
            "Status",
            ["Active", "Recovered", "Critical"],
            index=["Active", "Recovered", "Critical"].index(patient["status"])
        )

        submitted = st.form_submit_button("Save Changes")

        if submitted:
            data = {
                "name": name,
                "age": age,
                "gender": gender,
                "blood_group": patient["blood_group"],
                "phone": phone,
                "emergency_contact": emergency_contact,
                "address": address,
                "insurance_policy": insurance_policy,
                "coverage_percent": patient["coverage_percent"],
                "status": status,
                "last_visited": str(date.today())
            }

            update_patient(patient["id"], data)
            st.success("Patient updated successfully")
            st.rerun()


# ---------------- MAIN PAGE ----------------
def show_patients():

    st.title("👨‍⚕️ Patients")

    col_search, col_add = st.columns([3, 1])

    with col_search:
        query = st.text_input("", placeholder="🔍 Search patient by name")

    with col_add:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("➕ Add Patient", use_container_width=True):
            add_patient_dialog()

    df = get_patients()

    if query:
        df = df[df["name"].str.contains(query, case=False)]

    if df.empty:
        st.info("No patients found")
        return

    cols = st.columns(3)

    for i, row in df.iterrows():
        with cols[i % 3]:
            with st.container(border=True):

                st.markdown(f"### {row['name']}")
                st.markdown(f"**Age:** {row['age']}")
                st.markdown(f"**Gender:** {row['gender']}")
                st.markdown(f"**Phone:** {row['phone']}")
                st.markdown(f"**Last Visited:** {row['last_visited']}")

                if st.button("✏️ Edit", key=f"edit_{row['id']}"):
                    edit_patient_dialog(row)
