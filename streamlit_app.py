import streamlit as st
import pickle
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

# Load model and vectorizer
with open('phishing_detector_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open('tfidf_vectorizer.pkl', 'rb') as vec_file:
    vectorizer = pickle.load(vec_file)

# Streamlit app setup
st.set_page_config(page_title="Phish & Destroy", page_icon="🎣")
st.title("🛡️ Phish & Destroy")

# App mode selection
mode = st.radio("Choose a tool:", ["📧 Phishing Email Detector", "🔐 Password Strength Checker"])

# =============================
# 📧 Email Phishing Detection
# =============================
if mode == "📧 Phishing Email Detector":
    st.subheader("Detect Suspicious Emails")
    email_text = st.text_area("📩 Paste email content:", height=250)

    if st.button("🔍 Check for Phishing"):
        if email_text.strip() == "":
            st.warning("Please enter some email content.")
        else:
            # You might need to replicate any additional feature engineering here
            X_input = vectorizer.transform([email_text])
            prediction = model.predict(X_input)[0]

            if prediction == 1:
                st.error("⚠️ This email looks like **Phishing**!")
            else:
                st.success("✅ This email seems **Legitimate**.")

# =============================
# 🔐 Password Strength Checker
# =============================
elif mode == "🔐 Password Strength Checker":
    st.subheader("Check Your Password Strength")

    password = st.text_input("Enter a password to check:", type="password")

    def check_strength(pw):
        length = len(pw) >= 8
        upper = re.search(r"[A-Z]", pw) is not None
        lower = re.search(r"[a-z]", pw) is not None
        digit = re.search(r"\d", pw) is not None
        special = re.search(r"[!@#$%^&*(),.?\":{}|<>]", pw) is not None

        score = sum([length, upper, lower, digit, special])
        return score

    if st.button("🔍 Check Strength"):
        if password == "":
            st.warning("Please enter a password.")
        else:
            score = check_strength(password)
            if score <= 2:
                st.error("🟥 Weak Password")
            elif score == 3 or score == 4:
                st.warning("🟨 Moderate Password")
            else:
                st.success("🟩 Strong Password")

# Footer
st.markdown("---")
st.caption("Built with ❤️ using Streamlit, scikit-learn, and regex")
