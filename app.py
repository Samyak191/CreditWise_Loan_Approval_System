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
    credit_score = st.slider("Credit Score", 300, 900, 650)

with col2:
    employment = st.selectbox("Employment Status", ["Salaried", "Self-employed"])
    education = st.selectbox("Education", ["Graduate", "Not Graduate"])
    marital_status = st.selectbox("Marital Status", ["Single", "Married"])

# ---------------- Create Input ----------------
input_data = pd.DataFrame(columns=trained_columns)
input_data.loc[0] = 0

# Fill main features (⚠️ names must match your dataset)
input_data["ApplicantIncome"] = income
input_data["LoanAmount"] = loan_amount
input_data["Credit_Score"] = credit_score

# Handle categorical (⚠️ match names)
if employment == "Salaried":
    input_data["Employment_Salaried"] = 1
else:
    input_data["Employment_Self-employed"] = 1

if education == "Graduate":
    input_data["Education_Graduate"] = 1

if marital_status == "Married":
    input_data["Marital_Status_Married"] = 1

# ---------------- Prediction ----------------
if st.button("Predict Loan Approval"):

    input_scaled = scaler.transform(input_data)

    prediction = model.predict(input_scaled)

    if prediction[0] == 1:
        st.success("✅ Loan Approved")
    else:
        st.error("❌ Loan Rejected")