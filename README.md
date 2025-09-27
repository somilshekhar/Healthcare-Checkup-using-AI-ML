# 🏥 Healthcare Disease Prediction

[![Python](https://img.shields.io/badge/python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.26-orange?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

A **Streamlit-based web application** that predicts the likelihood of a disease (e.g., diabetes) based on patient data. Supports **PDF uploads** and **manual input** for healthcare reports.

---

## 🚀 Demo



https://github.com/user-attachments/assets/c04351ee-377b-4b52-8859-d2039ffb789e


---

## 🌟 Features

- **PDF Upload** – Extracts relevant patient features automatically from reports.  
- **Manual Input** – Enter patient details if a PDF isn’t available.  
- **ML Prediction** – Uses a trained machine learning model for disease prediction.  
- **Preprocessing** – Handles missing values and scales inputs to match training.  
- **Interactive UI** – Built with Streamlit for real-time predictions.  

---

## 💻 Installation

```bash
git clone https://github.com/somilshekhar/health-prediction.git
cd health-prediction
python -m venv .venv
# Activate your virtual environment:
# Windows PowerShell
.venv\Scripts\Activate.ps1
# Windows CMD
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt


⚡ Usage
in git bash-(run command)-

streamlit run app.py


1.Upload a PDF report or enter patient details manually.

2.Click Predict to see the result.

3.Result shows if the patient is likely or unlikely to have the disease.

📊 Example Input Values

| Feature                    | Example Value |
| -------------------------- | ------------- |
| Pregnancies                | 1             |
| Glucose                    | 100           |
| Blood Pressure             | 120           |
| Skin Thickness             | 20            |
| Insulin                    | 80            |
| BMI                        | 25.00         |
| Diabetes Pedigree Function | 0.5000        |
| Age                        | 30            |

🗂 File Structure
health-prediction/
│
├── app.py                 # Main Streamlit app
├── best_model.pkl         # Pre-trained ML model
├── scaler.pkl             # Scaler for preprocessing
├── training_medians.pkl   # Median values for missing data
├── requirements.txt       # Python dependencies
└── README.md


⚠ Disclaimer

This app is for educational/testing purposes only.
It is not medical advice. Consult a healthcare professional for medical concerns.

[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

