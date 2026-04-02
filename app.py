import streamlit as st
import time
import numpy as np
from PIL import Image
from pyzbar.pyzbar import decode
import qrcode
from datetime import datetime, timedelta

st.set_page_config(page_title="HemoTrack AI System", page_icon="🩸", layout="centered")

# ---------------- UI DESIGN ----------------
st.markdown("""
    <style>
    body {
        background-color: #f5f7fa;
    }

    .main {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
    }

    h1, h2, h3 {
        text-align: center;
    }

    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 45px;
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "page" not in st.session_state:
    st.session_state.page = "splash"

# ---------------- QR FUNCTION ----------------
def read_qr_safe(image):
    try:
        decoded = decode(image)
        if not decoded:
            return "NO_QR", None

        data = decoded[0].data.decode("utf-8")

        parsed = {}
        for item in data.split("|"):
            if ":" in item:
                key, value = item.split(":")
                parsed[key.strip()] = value.strip()

        return "VALID_QR", parsed

    except:
        return "INVALID_QR", None

# ---------------- COLOR DETECTION (UNCHANGED LOGIC) ----------------
def detect_blood_type(image):
    img = np.array(image)
    img = img / 255.0

    r = img[:, :, 0]
    g = img[:, :, 1]
    b = img[:, :, 2]

    red_mask = (r > 0.35) & (r > g) & (r > b)
    red_pixels = np.sum(red_mask)

    if red_pixels < 100:
        return "No Blood Detected ⚠️", 50

    blood_pixels = img[red_mask]

    avg_color = np.mean(blood_pixels, axis=0)
    r_avg, g_avg, b_avg = avg_color
    brightness = np.mean(avg_color)

    if brightness < 0.25:
        return "Severely Degraded Blood 🔴", 90
    elif r_avg > 0.6 and brightness > 0.45:
        return "Normal Blood 🟢", 20
    else:
        return "Hemolyzed Blood 🟡", 60

# ---------------- EXPIRY (UNCHANGED LOGIC) ----------------
def check_expiry(qr_data):
    try:
        collection_date = qr_data.get("CollectionDate", None)

        if not collection_date:
            return "Unknown ⚠️", 50

        collection_dt = datetime.strptime(collection_date, "%Y-%m-%d")
        expiry_dt = collection_dt + timedelta(days=42)
        today = datetime.today()

        if today > expiry_dt:
            return "Expired 🔴", 90
        else:
            days_left = (expiry_dt - today).days
            return f"Valid ({days_left} days left) 🟢", 10

    except:
        return "Invalid Date ⚠️", 60

# ---------------- SPLASH ----------------
if st.session_state.page == "splash":
    st.markdown("<h1>🩸 HemoTrack</h1>", unsafe_allow_html=True)
    st.markdown("<h3>AI-Based Blood Safety Monitoring System</h3>", unsafe_allow_html=True)

    st.image("https://cdn-icons-png.flaticon.com/512/2966/2966485.png", width=120)

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
    st.markdown("## Select System Mode")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🧑‍🔬 Technician Panel"):
            st.session_state.page = "tech"
            st.rerun()

    with col2:
        if st.button("📷 Scan Blood Bag"):
            st.session_state.page = "scan"
            st.rerun()

# ---------------- TECHNICIAN ----------------
elif st.session_state.page == "tech":

    if st.button("⬅ Back"):
        st.session_state.page = "menu"
        st.rerun()

    st.markdown("## 🧑‍🔬 Technician Panel")

    blood_group = st.text_input("Blood Group (e.g., B+)")
    collection_date = st.text_input("Collection Date (YYYY-MM-DD)")
    donor_id = st.text_input("Donor ID")

    if st.button("Generate QR"):

        if blood_group and collection_date and donor_id:
            data = f"BloodGroup:{blood_group}|CollectionDate:{collection_date}|DonorID:{donor_id}|Status:Valid"

            qr = qrcode.make(data)
            st.image(qr, caption="Generated QR Code")

            st.success("QR Generated Successfully")
        else:
            st.warning("Please fill all fields")

# ---------------- SCANNING ----------------
elif st.session_state.page == "scan":

    if st.button("⬅ Back"):
        st.session_state.page = "menu"
        st.rerun()

    st.markdown("## 📷 Blood Bag Analysis")

    uploaded_file = st.file_uploader("Upload Blood Bag Image", type=["jpg", "png", "jpeg"])

    if uploaded_file:

        image = Image.open(uploaded_file)
        img = np.array(image)

        st.image(image, caption="Uploaded Image", use_column_width=True)

        st.markdown("---")

        # QR Detection
        qr_status, qr_data = read_qr_safe(img)

        st.subheader("🔳 QR Detection")

        if qr_status == "NO_QR":
            st.warning("QR Code Not Visible")
            expiry_risk = 50

        elif qr_status == "INVALID_QR":
            st.info("QR Detected but Unreadable")
            expiry_risk = 50

        else:
            st.success("QR Code Detected")
            st.write(qr_data)

            expiry_status, expiry_risk = check_expiry(qr_data)

            st.subheader("📅 Expiry Status")
            st.write(expiry_status)

        # Blood Detection
        condition, color_risk = detect_blood_type(img)

        # UI DISPLAY (IMPROVED ONLY)
        st.markdown("### 🔍 Analysis Report")
        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Blood Condition", condition)

        with col2:
            st.metric("Risk Level", f"{max(color_risk, expiry_risk)}%")

        risk = max(color_risk, expiry_risk)

        st.progress(risk)

        st.markdown("---")

        # Final Decision
        st.subheader("🚨 Final Diagnosis")

        if risk < 30:
            st.success("🟢 SAFE TO USE")

        elif risk < 70:
            st.warning("🟡 DO NOT PREFER")

        else:
            st.error("🔴 REJECT - EXPIRED OR DAMAGED")

        st.markdown("---")
        st.info("Analysis Complete")

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown(
    "<p style='text-align:center;'>Developed by Biomedical Engineering Student | HemoTrack AI System</p>",
    unsafe_allow_html=True
)