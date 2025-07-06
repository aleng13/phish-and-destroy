import streamlit as st
import pickle
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import hstack
from sklearn.preprocessing import StandardScaler
from streamlit_lottie import st_lottie
import requests

# Load model and vectorizer (using enhanced filenames)
with open('phishing_detector_model_enhanced.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open('tfidf_vectorizer_enhanced.pkl', 'rb') as vec_file:
    vectorizer = pickle.load(vec_file)

try:
    with open('feature_scaler_enhanced.pkl', 'rb') as scaler_file:
        scaler = pickle.load(scaler_file)
except FileNotFoundError:
    st.error("Error: 'feature_scaler_enhanced.pkl' not found. This file is crucial for scaling numerical features correctly.")
    st.stop()

common_passwords = ["123456", "password", "123456789", "qwerty", "abc123"]

def check_password_strength_advanced(password):
    tips = []
    passed_checks = 0
    total_checks = 6

    if len(password) >= 8:
        passed_checks += 1
    else:
        tips.append("🔴 Make it at least 8 characters long")

    if re.search(r"\d", password):
        passed_checks += 1
    else:
        tips.append("🔴 Add at least one digit (0–9)")

    if re.search(r"[A-Z]", password):
        passed_checks += 1
    else:
        tips.append("🔴 Add an uppercase letter (A–Z)")

    if re.search(r"[a-z]", password):
        passed_checks += 1
    else:
        tips.append("🔴 Add a lowercase letter (a–z)")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        passed_checks += 1
    else:
        tips.append("🔴 Include at least one symbol (e.g., @, #, !)")

    if password.lower() not in common_passwords:
        passed_checks += 1
    else:
        tips.append("🔴 Avoid common passwords like '123456' or 'password'")

    score = int((passed_checks / total_checks) * 100)
    if score == 100:
        strength = "🟩 Strong"
    elif score >= 60:
        strength = "🟨 Moderate"
    else:
        strength = "🟥 Weak"

    return strength, tips, score

def extract_features(text):
    cleaned_for_tfidf = text.strip().lower()
    tfidf_vector = vectorizer.transform([cleaned_for_tfidf])
    email_length = len(text)
    num_exclamations = text.count('!')
    num_links = text.lower().count('http') + text.lower().count('www')
    num_uppercase_words = sum(1 for word in text.split() if word.isupper())
    num_special_chars = sum(1 for char in text if not char.isalnum() and not char.isspace())
    raw_numeric_features = np.array([[email_length, num_exclamations, num_links, num_uppercase_words, num_special_chars]])
    scaled_numeric_features = scaler.transform(raw_numeric_features)
    final_features = hstack([tfidf_vector, scaled_numeric_features])
    return final_features

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

st.set_page_config(page_title="Phish & Destroy", page_icon="🎣")

lottie_phish = load_lottieurl("https://assets1.lottiefiles.com/private_files/lf30_vnseqwqr.json")
if lottie_phish:
    st_lottie(lottie_phish, height=250, key="phishing_lottie")

st.markdown("""
    <h1 style='text-align: center;'>🎣 Phish & Destroy</h1>
    <p style='text-align: center;'>Your friendly AI tool to fight phishing and bad passwords.</p>
    <hr style='border: 1px solid #ddd;'>
""", unsafe_allow_html=True)

with st.expander("❓ What is Phishing?"):
    st.markdown("""
    Phishing is a fraudulent attempt to obtain sensitive information by disguising as a trustworthy entity in digital communication.

    ### 🧨 Dangers of Phishing:
    - Identity theft
    - Financial loss
    - Account compromise
    - Malware/ransomware attacks

    ### 🛡️ How This Tool Helps:
    - Uses machine learning to detect potential phishing emails
    - Gives instant feedback to help you avoid falling for scams
    - Helps you use strong, unbreakable passwords
    """)

# --- Tabs ---
tab1, tab2 = st.tabs(["📧 Email Phishing Detector", "🔐 Password Checker"])

with tab1:
    st.markdown("Enter email content and check if it's phishing or not.")

    email_text = st.text_area("📝 Paste email content here:", height=250, key="example_email")

    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("🚨 Detect Phishing"):
            if st.session_state["example_email"].strip() == "":
                st.warning("Please enter some email content.")
            else:
                try:
                    X_input = extract_features(st.session_state["example_email"])
                    prediction = model.predict(X_input)[0]
                    if prediction == 1:
                        st.error("⚠️ This email looks like **Phishing**!")
                    else:
                        st.success("✅ This email seems **Legitimate**.")
                    st.toast("Prediction complete! ✅")
                except Exception as e:
                    st.error(f"Error during prediction: {e}.")
                    st.exception(e)
    with col2:
        if st.button("❌ Clear Text"):
            st.session_state["example_email"] = ""
    with col3:
        if st.button("📋 Try Example Email"):
            st.session_state["example_email"] = "Dear user, your account has been suspended. Please click the link below to verify your account immediately. http://phishy.fake/login"

with tab2:
    st.markdown("Enter a password and get instant feedback on how strong it is.")

    password = st.text_input("🔑 Enter your password:", type="password")

    if st.button("🧠 Analyze Strength"):
        if password == "":
            st.warning("Please enter a password.")
        else:
            strength, suggestions, score = check_password_strength_advanced(password)
            st.markdown(f"### Strength: {strength} ({score}%)")
            st.progress(score)
            if suggestions:
                st.markdown("**💡 Suggestions to Improve:**")
                for tip in suggestions:
                    st.write(f"- {tip}")
            else:
                st.success("Perfect! Your password is very strong. 🏆")
            st.toast("Password analyzed! ✅")

st.markdown("""
---
<p style='text-align: center;'>Built with ❤️ by Alen using Streamlit, scikit-learn and Python 🐍</p>
""", unsafe_allow_html=True)
