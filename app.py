import streamlit as st
import pickle
import pandas as pd

# Load model, scaler, columns
model = pickle.load(open("model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))
trained_columns = pickle.load(open("columns.pkl", "rb"))

st.title("🏦 CreditWise Loan Approval System")
st.write("Enter Applicant Details")

# ---------------- UI ----------------
col1, col2 = st.columns(2)

with col1:
    income = st.number_input("Applicant Income", min_value=0)
    loan_amount = st.number_input("Loan Amount", min_value=0)

with col2:
    employment = st.selectbox("Employment Status", ["Salaried", "Self-employed"])
    education = st.selectbox("Education", ["Graduate", "Not Graduate"])
    marital_status = st.selectbox("Marital Status", ["Single", "Married"])

# Additional IMPORTANT inputs
dependents = st.selectbox("Dependents", ["0", "1", "2", "3+"])
property_area = st.selectbox("Property Area", ["Urban", "Semiurban", "Rural"])
credit_history = st.selectbox("Credit History", ["Good", "Bad"])

# ---------------- Create Input ----------------
input_data = pd.DataFrame(columns=trained_columns)
input_data.loc[0] = 0

# Fill numerical
if "ApplicantIncome" in trained_columns:
    input_data["ApplicantIncome"] = income

if "LoanAmount" in trained_columns:
    input_data["LoanAmount"] = loan_amount

# ---------------- Categorical Encoding ----------------

# Employment
for col in trained_columns:
    if "Employment" in col:
        input_data[col] = 0

if "Employment_Salaried" in trained_columns and employment == "Salaried":
    input_data["Employment_Salaried"] = 1

if "Employment_Self-employed" in trained_columns and employment == "Self-employed":
    input_data["Employment_Self-employed"] = 1

# Education
if "Education_Graduate" in trained_columns:
    input_data["Education_Graduate"] = 1 if education == "Graduate" else 0

# Marital Status
if "Marital_Status_Married" in trained_columns:
    input_data["Marital_Status_Married"] = 1 if marital_status == "Married" else 0

# Dependents
if "Dependents" in trained_columns:
    input_data["Dependents"] = int(dependents.replace("+", ""))

# Property Area
for col in trained_columns:
    if "Property_Area" in col:
        input_data[col] = 0

if "Property_Area_Urban" in trained_columns and property_area == "Urban":
    input_data["Property_Area_Urban"] = 1

if "Property_Area_Semiurban" in trained_columns and property_area == "Semiurban":
    input_data["Property_Area_Semiurban"] = 1

if "Property_Area_Rural" in trained_columns and property_area == "Rural":
    input_data["Property_Area_Rural"] = 1

# Credit History (MOST IMPORTANT)
for col in trained_columns:
    if "Credit_History" in col:
        input_data[col] = 1 if credit_history == "Good" else 0

# Default values
if "Loan_Amount_Term" in trained_columns:
    input_data["Loan_Amount_Term"] = 360

if "CoapplicantIncome" in trained_columns:
    input_data["CoapplicantIncome"] = 0

if "Self_Employed" in trained_columns:
    input_data["Self_Employed"] = 0

# ---------------- Prediction ----------------
if st.button("Predict Loan Approval"):

    # Ensure correct order
    input_data = input_data[trained_columns]

    input_scaled = scaler.transform(input_data)

    prediction = model.predict(input_scaled)
    probability = model.predict_proba(input_scaled)[0][1]

    if prediction[0] == 1:
        st.success(f"✅ Loan Approved (Probability: {probability:.2f})")
    else:
        st.error(f"❌ Loan Not Approved (Probability: {probability:.2f})")