import streamlit as st
import pickle

# Load model
model = pickle.load(open("model.pkl", "rb"))

st.title("CreditWise Loan Approval System")

st.write("Enter details to check loan approval")

income = st.number_input("Income")
loan_amount = st.number_input("Loan Amount")

if st.button("Predict"):
    prediction = model.predict([[income, loan_amount]])
    
    if prediction[0] == 1:
        st.success("✅ Loan Approved")
    else:
        st.error("❌ Loan Rejected")