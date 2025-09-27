# ===============================
# Healthcare Disease Prediction App
# ===============================

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import fitz  # PyMuPDF for PDF processing
import re   # Regular expressions for text parsing

# ===============================
# --- Load Model, Scaler, Medians ---
# ===============================
def load_assets():
    try:
        with open('best_model.pkl', 'rb') as f:
            model = pickle.load(f)
        with open('scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)
        with open('training_medians.pkl', 'rb') as f:
            medians = pickle.load(f)
        return model, scaler, medians
    except FileNotFoundError:
        st.error(
            "Error: Model, scaler, or training medians file not found. "
            "Please ensure 'best_model.pkl', 'scaler.pkl', and 'training_medians.pkl' are in the same directory."
        )
        st.stop()

# Load assets
model, scaler, training_medians = load_assets()

# ===============================
# --- App Title & Instructions ---
# ===============================
st.title('Healthcare Disease Prediction')
st.write('Upload a healthcare report PDF to get a disease prediction, or enter details manually.')

# ===============================
# --- Feature Extraction ---
# ===============================
def extract_features_from_text(text):
    """Extracts healthcare features from PDF text using regex."""
    extracted_data = {}
    text = text.lower()

    patterns = {
        'pregnancies': r'pregnanc(?:y|ies)\s*[:=]?\s*(\d+)',
        'glucose': r'glucose\s*(?:level)?\s*[:=]?\s*(\d+)',
        'blood_pressure': r'(?:blood\s*pressure|bp)\s*[:=]?\s*(\d+)',
        'skin_thickness': r'(?:skin\s*thickness|triceps\s*skin\s*fold\s*thickness)\s*[:=]?\s*(\d+)',
        'insulin': r'insulin\s*(?:level)?\s*[:=]?\s*(\d+)',
        'bmi': r'bmi\s*[:=]?\s*(\d+\.?\d*)',
        'diabetes_pedigree_function': r'(?:diabetes\s*pedigree\s*function|dpf)\s*[:=]?\s*(\d+\.?\d*)',
        'age': r'age\s*[:=]?\s*(\d+)'
    }

    for feature, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            try:
                extracted_data[feature] = float(match.group(1)) if '.' in match.group(1) else int(match.group(1))
            except ValueError:
                extracted_data[feature] = None
                st.warning(f"Could not convert '{feature}' value: {match.group(1)}")
        else:
            extracted_data[feature] = None
            st.warning(f"Could not find '{feature}' in the uploaded report.")
    return extracted_data

# ===============================
# --- Prediction Function ---
# ===============================
def make_prediction(input_df, scaler, model, medians):
    """Preprocesses input and predicts disease."""
    cols_to_impute = ['glucose', 'blood_pressure', 'skin_thickness', 'insulin', 'bmi']
    input_df[cols_to_impute] = input_df[cols_to_impute].replace(0, np.nan)
    for col in cols_to_impute:
        if col in input_df.columns:
            input_df[col].fillna(medians[col], inplace=True)

    input_scaled = scaler.transform(input_df)
    prediction = model.predict(input_scaled)
    return prediction

# ===============================
# --- PDF Upload Section ---
# ===============================
uploaded_file = st.file_uploader("Upload Healthcare Report (PDF)", type=['pdf'])

if uploaded_file is not None:
    st.write("File uploaded successfully! Extracting text...")
    try:
        pdf_document = fitz.open(stream=uploaded_file.getvalue(), filetype="pdf")
        full_text = ""
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            full_text += page.get_text()

        st.write("Text extracted from PDF:")
        st.text_area("Extracted Text", full_text, height=300, disabled=True)

        extracted_features = extract_features_from_text(full_text)

        st.subheader("Extracted Features from PDF")
        display_data = {k.replace('_', ' ').title(): v for k, v in extracted_features.items()}
        st.write(pd.DataFrame([display_data]).T.rename(columns={0: "Value"}))

        # Check missing features
        required_features = ['pregnancies','glucose','blood_pressure','skin_thickness','insulin','bmi','diabetes_pedigree_function','age']
        missing_features = [f for f in required_features if extracted_features.get(f) is None]

        input_data_pdf = pd.DataFrame([extracted_features])[required_features]

        if missing_features:
            st.warning(f"Missing features: {', '.join([f.replace('_',' ').title() for f in missing_features])}")
            manual_inputs = {}
            st.subheader("Manual Input for Missing Features")
            for feature in missing_features:
                if feature in ['pregnancies', 'blood_pressure', 'skin_thickness', 'insulin', 'age']:
                    manual_inputs[feature] = st.number_input(f'{feature.replace("_"," ").title()}', min_value=0, value=0, key=f'manual_pdf_{feature}')
                elif feature in ['glucose']:
                    manual_inputs[feature] = st.number_input(f'{feature.replace("_"," ").title()}', min_value=0, max_value=200, value=100, key=f'manual_pdf_{feature}')
                elif feature in ['bmi', 'diabetes_pedigree_function']:
                    manual_inputs[feature] = st.number_input(f'{feature.replace("_"," ").title()}', min_value=0.0, value=0.0, format="%.4f", key=f'manual_pdf_{feature}')

            if st.button('Predict (PDF + Manual Input)'):
                final_input_data_dict = {**extracted_features, **manual_inputs}
                input_data_combined = pd.DataFrame([final_input_data_dict])[required_features]
                try:
                    prediction = make_prediction(input_data_combined, scaler, model, training_medians)
                    st.subheader("Prediction Result")
                    if prediction[0] == 1:
                        st.error('Prediction: The patient is likely to have the disease.')
                    else:
                        st.success('Prediction: The patient is unlikely to have the disease.')
                except Exception as e:
                    st.error(f"Error during prediction: {e}")

        else:
            try:
                prediction = make_prediction(input_data_pdf, scaler, model, training_medians)
                st.subheader("Prediction Result")
                if prediction[0] == 1:
                    st.error('Prediction: The patient is likely to have the disease.')
                else:
                    st.success('Prediction: The patient is unlikely to have the disease.')
            except Exception as e:
                st.error(f"Error during prediction: {e}")

    except Exception as e:
        st.error(f"Error processing PDF: {e}")

# ===============================
# --- Manual Input Section ---
# ===============================
st.write('---')
st.subheader("Enter Details Manually")

manual_input_values = {
    'pregnancies': st.number_input('Pregnancies', min_value=0, max_value=20, value=1, key='manual_pregnancies_input'),
    'glucose': st.number_input('Glucose', min_value=0, max_value=200, value=100, key='manual_glucose_input'),
    'blood_pressure': st.number_input('Blood Pressure', min_value=0, max_value=120, value=70, key='manual_blood_pressure_input'),
    'skin_thickness': st.number_input('Skin Thickness', min_value=0, max_value=100, value=20, key='manual_skin_thickness_input'),
    'insulin': st.number_input('Insulin', min_value=0, max_value=900, value=80, key='manual_insulin_input'),
    'bmi': st.number_input('BMI', min_value=0.0, max_value=60.0, value=25.0, key='manual_bmi_input'),
    'diabetes_pedigree_function': st.number_input('Diabetes Pedigree Function', min_value=0.0, max_value=2.5, value=0.5, format="%.4f", key='manual_dpf_input'),
    'age': st.number_input('Age', min_value=0, max_value=120, value=30, key='manual_age_input')
}

if st.button('Predict (Manual Input)', key='manual_predict_button'):
    input_data_manual = pd.DataFrame([list(manual_input_values.values())], columns=list(manual_input_values.keys()))
    try:
        prediction_manual = make_prediction(input_data_manual, scaler, model, training_medians)
        st.subheader("Prediction Result")
        if prediction_manual[0] == 1:
            st.error('Prediction (Manual Input): The patient is likely to have the disease.')
        else:
            st.success('Prediction (Manual Input): The patient is unlikely to have the disease.')
    except Exception as e:
        st.error(f"Error during manual prediction: {e}")

# ===============================
# --- Disclaimer ---
# ===============================
st.write('Note: This is a prediction based on a trained model and should not be considered medical advice.')
