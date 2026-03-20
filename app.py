import streamlit as st
import pickle
import numpy as np

# Load model & scaler
model = pickle.load(open("model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

st.title("CreditWise Loan Approval System")

st.write("Enter details")

# ⚠️ TEMP: use same number of inputs as your model
# (we'll refine after you confirm feature count)

income = st.number_input("Income")
loan_amount = st.number_input("Loan Amount")

# 👉 Dummy extra inputs (IMPORTANT)
feature3 = st.number_input("Feature 3")
feature4 = st.number_input("Feature 4")

if st.button("Predict"):
    input_data = np.array([[income, loan_amount, feature3, feature4]])
    
    input_scaled = scaler.transform(input_data)
    
    prediction = model.predict(input_scaled)

    if prediction[0] == 1:
        st.success("✅ Loan Approved")
    else:
        st.error("❌ Loan Rejected")