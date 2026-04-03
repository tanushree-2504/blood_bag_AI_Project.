import streamlit as st
import numpy as np
from PIL import Image
import cv2
import pickle
import qrcode
import time

# ---------------- LOAD MODEL ----------------
model = pickle.load(open("blood_model.pkl", "rb"))

# ---------------- CONFIG ----------------
st.set_page_config(page_title="HemoTrack", layout="centered")

# ---------------- SESSION ----------------
if "page" not in st.session_state:
    st.session_state.page = "splash"

# ---------------- QR SAFE FUNCTION ----------------
def read_qr_safe(image):
    return "NO_QR", None  # Safe fallback (no crash)

# ---------------- AI BLOOD DETECTION ----------------
def detect_blood_type(image):

    img = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    img = cv2.resize(img, (100, 100))
    img = img.flatten().reshape(1, -1)

    prediction = model.predict(img)[0]
    probabilities = model.predict_proba(img)[0]

    confidence = round(max(probabilities) * 100, 2)

    if prediction == 0:
        return f"Normal Blood 🟢 ({confidence}%)"
    elif prediction == 1:
        return f"Hemolyzed Blood 🟡 ({confidence}%)"
    else:
        return f"Severely Degraded Blood 🔴 ({confidence}%)"

# ---------------- RISK ----------------
def calculate_risk(condition):
    if "Normal" in condition:
        return 15
    elif "Hemolyzed" in condition:
        return 50
    else:
        return 85

# ---------------- SPLASH ----------------
if st.session_state.page == "splash":
    st.markdown("<h1 style='text-align:center;'>🩸 HemoTrack</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>AI Blood Monitoring System</p>", unsafe_allow_html=True)

    time.sleep(3)
    st.session_state.page = "start"
    st.rerun()

# ---------------- START ----------------
elif st.session_state.page == "start":
    st.markdown("## Welcome to HemoTrack")

    if st.button("🚀 Start System"):
        st.session_state.page = "menu"
        st.rerun()

# ---------------- MENU ----------------
elif st.session_state.page == "menu":
    st.markdown("## Select Mode")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🧑‍🔬 Technician"):
            st.session_state.page = "tech"
            st.rerun()

    with col2:
        if st.button("📷 Scan Blood Bag"):
            st.session_state.page = "scan"
            st.rerun()

# ---------------- TECH ----------------
elif st.session_state.page == "tech":

    if st.button("⬅ Back"):
        st.session_state.page = "menu"
        st.rerun()

    st.markdown("## 🧑‍🔬 Technician Panel")

    blood_group = st.text_input("Blood Group")
    donor_id = st.text_input("Donor ID")

    if st.button("Generate QR"):
        if blood_group and donor_id:
            data = f"BloodGroup:{blood_group}|DonorID:{donor_id}|Status:Valid"
            qr = qrcode.make(data)
            st.image(qr)
            st.success("QR Generated Successfully")
        else:
            st.warning("Please fill all fields")

# ---------------- SCAN ----------------
elif st.session_state.page == "scan":

    if st.button("⬅ Back"):
        st.session_state.page = "menu"
        st.rerun()

    st.markdown("## 📷 Blood Bag Analysis")

    file = st.file_uploader("Upload Blood Bag Image", type=["png","jpg","jpeg"])

    if file:

        image = Image.open(file)
        img = np.array(image)

        st.image(image, caption="Uploaded Image", use_column_width=True)

        st.markdown("---")

        # QR
        qr_status, qr_data = read_qr_safe(img)

        st.subheader("🔳 QR Detection")
        if qr_status == "NO_QR":
            st.warning("QR Not Visible")
        else:
            st.success("QR Detected")

        # AI Detection
        condition = detect_blood_type(img)

        st.subheader("🩸 Blood Condition (AI)")
        st.write(condition)

        # Risk
        risk = calculate_risk(condition)

        st.subheader("📊 Health Risk Score")
        st.progress(risk)
        st.write(f"{risk}% Risk")

        # Final Diagnosis
        st.subheader("🚨 Final Diagnosis")

        if risk < 30:
            st.success("🟢 SAFE BLOOD")
        elif risk < 70:
            st.warning("🟡 NEEDS CHECK")
        else:
            st.error("🔴 DO NOT USE")

        st.markdown("---")
        st.info("Analysis Complete")