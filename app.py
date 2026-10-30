import re
from datetime import date
import streamlit as st
from pdf_generator import generate_pdf, APPLICATION_TYPES, DECLARATION
import db

st.set_page_config(page_title="Student Academic Requisition Form", page_icon="📝")
st.title("Student Academic Requisition Form")
st.caption("Fill in the details, accept the declaration, then generate and download the PDF.")

st.subheader("1. Student Details")
department = st.text_input("Name of Department *")
name = st.text_input("Student Name *")
c1, c2, c3 = st.columns(3)
roll = c1.text_input("Roll Number *")
semester = c2.selectbox("Semester *", [str(i) for i in range(1, 9)])
division = c3.text_input("Division *")
c4, c5 = st.columns(2)
email = c4.text_input("Email *")
mobile = c5.text_input("Mobile Number *", max_chars=10)
req_date = st.date_input("Date", value=date.today())

st.subheader("Application Type")
app_type = st.radio("Application for *", APPLICATION_TYPES, horizontal=True)
other_type = ""
if app_type == "Other request":
    other_type = st.text_input("Specify other request *")

st.subheader("2. Purpose / Brief Details of Request")
purpose = st.text_area("Purpose *", height=120)

st.subheader("3. Supporting Documents")
docs_attached = st.radio("Documents attached", ["Yes", "No"], index=1, horizontal=True)
doc_names = st.text_input("Document name(s)") if docs_attached == "Yes" else ""

st.subheader("4. Student Declaration")
st.info(DECLARATION)
agree = st.checkbox("I confirm the above declaration.")

if st.button("Generate PDF"):
    errors = []
    for label, val in [("Department", department), ("Student Name", name), ("Roll Number", roll),
                       ("Division", division), ("Purpose", purpose)]:
        if not val.strip():
            errors.append(f"{label} is required.")
    if app_type == "Other request" and not other_type.strip():
        errors.append("Please specify the other request.")
    if docs_attached == "Yes" and not doc_names.strip():
        errors.append("Please enter the supporting document name(s).")
    if not re.fullmatch(r"[6-9]\d{9}", mobile.strip()):
        errors.append("Mobile number must be a valid 10-digit number.")
    if not re.fullmatch(r"[\w.+-]+@[\w-]+(\.[\w-]+)+", email.strip()):
        errors.append("Enter a valid email address.")
    if not agree:
        errors.append("You must accept the student declaration.")

    if errors:
        for e in errors:
            st.error(e)
    else:
        data = dict(department=department.strip(), name=name.strip(), roll=roll.strip(),
                    semester=semester, division=division.strip(), email=email.strip(),
                    mobile=mobile.strip(), app_type=app_type, other_type=other_type.strip(),
                    purpose=purpose.strip(), docs_attached=docs_attached,
                    doc_names=doc_names.strip(), date=req_date.strftime("%d-%m-%Y"))
        db.save(data)
        st.session_state["pdf"] = generate_pdf(data)
        st.session_state["fname"] = (f"Requisition_{re.sub(r'[^A-Za-z0-9]+', '', data['roll'])}_"
                                     f"{re.sub(r'[^A-Za-z0-9]+', '_', data['name']).strip('_')}.pdf")
        st.success("Form submitted and PDF generated.")

if "pdf" in st.session_state:
    st.download_button("Download PDF", st.session_state["pdf"],
                       file_name=st.session_state["fname"], mime="application/pdf")
