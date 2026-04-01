# blood_bag_AI_Project.
# 🩸 HemoTrack – AI-Based Blood Bag Monitoring System

## 📌 Overview

**HemoTrack** is an AI-assisted healthcare application designed to monitor and analyze blood bag safety using computer vision and intelligent logic.
The system provides a **simple, reliable, and real-time interface** for both technicians and users to ensure blood quality and safety.

---

## 🎯 Objectives

* Automate blood bag inspection
* Reduce manual errors in blood banks
* Provide real-time safety feedback
* Enable digital traceability using QR codes
* Deliver a simple and reliable user interface

---

## 🧠 Key Features

### 🧑‍🔬 Technician Module

* Input blood bag details
* Generate QR codes for traceability
* Simple and quick data entry system

### 📷 Scanning Module

* Upload blood bag image
* Detect QR code (if present)
* Analyze blood condition using color detection
* Provide risk-based safety output

### 🔍 Smart QR Handling

* Detects QR if available
* Handles missing or invalid QR safely
* Ensures system never crashes

### 🩸 Blood Condition Analysis

* Classifies blood into:

  * Normal
  * Hemolyzed
  * Severely Degraded

### 📊 Risk Assessment

* Provides a risk score (0–100)
* Displays:

  * SAFE
  * NEEDS ATTENTION
  * HIGH RISK

---

## 🧭 System Workflow

1. Splash Screen (HemoTrack)
2. Start System
3. Select Mode:

   * Technician Panel
   * Blood Bag Scanning
4. Perform analysis and view results

---

## 🏗️ Project Structure

```
blood_ai_project/
│
├── app.py
├── requirements.txt
│
├── modules/
│   ├── __init__.py
│   ├── qr_module.py
│   ├── color_module.py
│   ├── risk_module.py
│
└── dataset/
    └── test_images2/
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/hemotrack.git
cd hemotrack
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the Application

```bash
streamlit run app.py
```

---

## 🌐 Deployment

The application can be deployed using **Streamlit Cloud**:

1. Push project to GitHub
2. Go to Streamlit Cloud
3. Select repository
4. Deploy `app.py`

---

## 🛠️ Technologies Used

* Python
* Streamlit
* OpenCV
* NumPy
* PIL (Pillow)
* pyzbar (QR detection)
* qrcode (QR generation)

---

## ⚠️ Limitations

* Color-based detection is heuristic (not CNN-based yet)
* AI-generated QR codes may not be scannable
* Performance depends on image quality and lighting

---

## 🚀 Future Scope

* Integration of CNN model for accurate classification
* Real-time camera scanning
* Cloud database integration
* Hospital-level deployment system

---

## 👩‍💻 Author

Developed as a Biomedical Engineering project focusing on AI-assisted healthcare safety systems.

---

## 📌 Note

This project is a prototype designed for academic and demonstration purposes.
It provides a foundation for developing real-world intelligent blood monitoring systems.

---
