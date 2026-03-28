import streamlit as st
import pickle
import pandas as pd

# ---------------- Load files ----------------
model = pickle.load(open("model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))
trained_columns = pickle.load(open("columns.pkl", "rb"))

# ---------------- UI ----------------
st.set_page_config(page_title="Loan Approval System", layout="wide")

st.title("🏦 CreditWise Loan Approval System")
st.write("Enter Applicant Details")
st.write(trained_columns)

col1, col2 = st.columns(2)

with col1:
    income = st.number_input("Applicant Income", min_value=0, value=50000)
    loan_amount = st.number_input("Loan Amount", min_value=0, value=200000)
    credit_score = st.slider("Credit Score", 300, 900, 650)

with col2:
    employment = st.selectbox("Employment Status", ["Salaried", "Self-employed"])
    education = st.selectbox("Education", ["Graduate", "Not Graduate"])
    marital_status = st.selectbox("Marital Status", ["Single", "Married"])

# ---------------- Create Input ----------------
input_data = pd.DataFrame(columns=trained_columns)
input_data.loc[0] = 0

# ---------------- Fill Main Features ----------------
input_data["ApplicantIncome"] = income
input_data["LoanAmount"] = loan_amount

# (⚠️ Only include this if it exists in your trained_columns)
if "Credit_Score" in trained_columns:
    input_data["Credit_Score"] = credit_score

# ---------------- Handle Categorical ----------------
if "Employment_Salaried" in trained_columns:
    input_data["Employment_Salaried"] = 1 if employment == "Salaried" else 0

if "Employment_Self-employed" in trained_columns:
    input_data["Employment_Self-employed"] = 1 if employment == "Self-employed" else 0

if "Education_Graduate" in trained_columns:
    input_data["Education_Graduate"] = 1 if education == "Graduate" else 0

if "Marital_Status_Married" in trained_columns:
    input_data["Marital_Status_Married"] = 1 if marital_status == "Married" else 0

# ---------------- Default Values (IMPORTANT FIX) ----------------
# These prevent model from assuming worst-case (0)

if "Credit_History" in trained_columns:
    input_data["Credit_History"] = 1

if "Loan_Amount_Term" in trained_columns:
    input_data["Loan_Amount_Term"] = 360

if "Dependents" in trained_columns:
    input_data["Dependents"] = 0

if "Self_Employed" in trained_columns:
    input_data["Self_Employed"] = 0

# ---------------- Prediction ----------------
if st.button("Predict Loan Approval"):

    # Ensure correct column order
    input_data = input_data[trained_columns]

    # Scale
    input_scaled = scaler.transform(input_data)

    # Predict
    prediction = model.predict(input_scaled)

    # Probability (bonus)
    try:
        prob = model.predict_proba(input_scaled)[0][1]
    except:
        prob = None

    # Output
    if prediction[0] == 1:
        st.success("✅ Loan Approved")
    else:
        st.error("❌ Loan Not Approved")

    if prob is not None:
        st.info(f"Approval Probability: {prob:.2f}")