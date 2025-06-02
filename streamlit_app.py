# streamlit_app.py

import streamlit as st
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Load the trained model and vectorizer
with open('final_phishing_detector.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open('tfidf_vectorizer.pkl', 'rb') as vec_file:
    vectorizer = pickle.load(vec_file)

# Streamlit UI
st.set_page_config(page_title="Phish & Destroy", page_icon="🎣")
st.title("🎣 Phish & Destroy - Email Phishing Detector")
st.write("Enter the content of an email below, and we'll let you know if it's **phishing** or **legitimate**.")

# Input box
email_text = st.text_area("📧 Paste your email content here:", height=250)

if st.button("🔍 Check for Phishing"):
    if email_text.strip() == "":
        st.warning("Please enter some email content.")
    else:
        # Vectorize the input
        X_input = vectorizer.transform([email_text])
        prediction = model.predict(X_input)[0]

        if prediction == 1:
            st.error("⚠️ This email looks like **Phishing**!")
        else:
            st.success("✅ This email seems **Legitimate**.")

# Optional: Footer or About section
st.markdown("---")
st.caption("Built with ❤️ using Streamlit and scikit-learn")
