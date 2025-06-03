import streamlit as st
import pickle
import re
from sklearn.feature_extraction.text import TfidfVectorizer

# Load model and vectorizer
with open('phishing_detector_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open('tfidf_vectorizer.pkl', 'rb') as vec_file:
    vectorizer = pickle.load(vec_file)

# Common passwords list
common_passwords = ["123456", "password", "123456789", "qwerty", "abc123"]

# Password checker function
def check_password_strength_advanced(password):
    tips = []
    passed_checks = 0
    total_checks = 6

    # 1. Length Check
    if len(password) >= 8:
        passed_checks += 1
    else:
        tips.append("🔴 Make it at least 8 characters long")

    # 2. Digit Check
    if re.search(r"\\d", password):
        passed_checks += 1
    else:
        tips.append("🔴 Add at least one digit (0–9)")

    # 3. Uppercase Check
    if re.search(r"[A-Z]", password):
        passed_checks += 1
    else:
        tips.append("🔴 Add an uppercase letter (A–Z)")

    # 4. Lowercase Check
    if re.search(r"[a-z]", password):
        passed_checks += 1
    else:
        tips.append("🔴 Add a lowercase letter (a–z)")

    # 5. Symbol Check
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        passed_checks += 1
    else:
        tips.append("🔴 Include at least one symbol (e.g., @, #, !)")

    # 6. Common Password Check
    if password.lower() not in common_passwords:
        passed_checks += 1
    else:
        tips.append("🔴 Avoid common passwords like '123456' or 'password'")

    # Score
    score = int((passed_checks / total_checks) * 100)
    if score == 100:
        strength = "🟩 Strong"
    elif score >= 60:
        strength = "🟨 Moderate"
    else:
        strength = "🟥 Weak"

    return strength, tips, score

# Streamlit setup
st.set_page_config(page_title="Phish & Destroy", page_icon="🎣")
st.markdown("""
    <h1 style='text-align: center;'>🎣 Phish & Destroy</h1>
    <p style='text-align: center;'>Your friendly AI tool to fight phishing and bad passwords.</p>
    <hr style='border: 1px solid #ddd;'>
""", unsafe_allow_html=True)

# Sidebar navigation
page = st.sidebar.selectbox("🔧 Choose a tool", ["Phishing Detector", "Password Strength Checker"])

# === Phishing Detection ===
if page == "Phishing Detector":
    st.subheader("📧 Email Phishing Detector")
    st.markdown("Enter email content and check if it's phishing or not.")

    email_text = st.text_area("📝 Paste email content here:", height=250)
    if st.button("🚨 Detect Phishing"):
        if email_text.strip() == "":
            st.warning("Please enter some email content.")
        else:
            try:
                X_input = vectorizer.transform([email_text])
                prediction = model.predict(X_input)[0]
                if prediction == 1:
                    st.error("⚠️ This email looks like **Phishing**!")
                else:
                    st.success("✅ This email seems **Legitimate**.")
            except Exception as e:
                st.error("Error during prediction. Make sure model/vectorizer match input features.")

# === Password Checker ===
elif page == "Password Strength Checker":
    st.subheader("🔐 Password Strength Checker")
    st.markdown("Enter a password and get instant feedback on how strong it is.")

    password = st.text_input("🔑 Enter your password:", type="password")

    if st.button("🧠 Analyze Strength"):
        if password == "":
            st.warning("Please enter a password.")
        else:
            strength, suggestions, score = check_password_strength_advanced(password)
            st.markdown(f"### Strength: {strength} ({score}%)")
            if suggestions:
                st.markdown("**💡 Suggestions to Improve:**")
                for tip in suggestions:
                    st.write(f"- {tip}")
            else:
                st.success("Perfect! Your password is very strong. 🏆")

# === Footer ===
st.markdown("""
---
<p style='text-align: center;'>Built with ❤️ by Alen using Streamlit, scikit-learn and Python 🐍</p>
""", unsafe_allow_html=True)
