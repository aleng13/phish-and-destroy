import streamlit as st
import pickle
import re
import numpy as np # Make sure numpy is imported
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import hstack # Make sure hstack is imported
from sklearn.preprocessing import StandardScaler # Make sure StandardScaler is imported for type hinting if needed

# Load model and vectorizer
with open('phishing_detector_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open('tfidf_vectorizer.pkl', 'rb') as vec_file:
    vectorizer = pickle.load(vec_file)

# Load the feature scaler
try:
    with open('feature_scaler.pkl', 'rb') as scaler_file:
        scaler = pickle.load(scaler_file)
except FileNotFoundError:
    st.error("Error: 'feature_scaler.pkl' not found. This file is crucial for scaling numerical features correctly.")
    st.stop() # Stop the app if scaler can't be loaded, as predictions will be wrong.

# Common passwords list
common_passwords = ["123456", "password", "123456789", "qwerty", "abc123"]
# Add the rest of your common passwords here, up to 20 if that's the desired max
# common_passwords = ["123456", "password", "123456789", "qwerty", "12345678", "111111", "12345", "password123", "admin", "welcome", "test", "qwerty123", "iloveyou", "p@ssword", "myself", "dragon", "football", "computer", "superman", "changeit"]


# Password checker function (keep this as is from your code)
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

# --- Feature engineering function (UPDATED) ---
def extract_features(text):
    # This part should mimic the preprocessing from your notebook for TF-IDF
    # Assuming you defined a preprocess_text function in your notebook before vectorizing
    # If not, use the raw text for numerical features, and a cleaned version for TF-IDF
    # For now, let's just use text for both, but adjust if your notebook had specific text cleaning *before* numerical feature extraction
    
    # Text preprocessing for TF-IDF
    # Assuming you had a 'cleaned_text' column in your DataFrame
    # If your numerical features were derived from the *original* raw text in the notebook,
    # then use the original 'text' variable directly for numerical feature extraction.
    # If they were derived from 'cleaned_text' after some cleaning, then use 'cleaned_text' here too.
    # Based on your previous snippet, num_uppercase_words uses original text, others use cleaned.
    
    # Define a simple text cleaning for TF-IDF here, similar to your notebook's 'cleaned_text'
    # This should match how df['cleaned_text'] was created in your notebook for TF-IDF
    cleaned_for_tfidf = text.strip().lower() # Basic cleaning
    # You might need more complex cleaning if your notebook had it (e.g., regex for links, punctuation, stopwords)

    # TF-IDF Vector
    tfidf_vector = vectorizer.transform([cleaned_for_tfidf]) # Use cleaned_for_tfidf for TF-IDF

    # Custom numeric features (mimic your notebook's 'extra_features' creation)
    # Be precise about whether these were derived from original text or a cleaned version.
    # Your notebook snippet showed 'df['cleaned_text'].apply(len)' for email_length, etc.
    # and 'text.split()' for num_uppercase_words. Let's assume the string passed to this function is the raw email.
    
    email_length = len(text) # Using original text for length
    num_exclamations = text.count('!') # Using original text
    num_links = text.lower().count('http') + text.lower().count('www') # Using original text
    num_uppercase_words = sum(1 for word in text.split() if word.isupper()) # Using original text
    num_special_chars = sum(1 for char in text if not char.isalnum() and not char.isspace()) # Using original text


    # Combine into a single array for scaling
    # IMPORTANT: Ensure the order of these features is EXACTLY the same as when you trained your scaler
    raw_numeric_features = np.array([[email_length, num_exclamations, num_links,
                                    num_uppercase_words, num_special_chars]])

    # --- APPLY SCALING TO NUMERICAL FEATURES ---
    # This is the missing step that causes the error!
    scaled_numeric_features = scaler.transform(raw_numeric_features)

    # Combine features (TF-IDF is sparse, numeric is dense - hstack handles this)
    final_features = hstack([tfidf_vector, scaled_numeric_features])

    return final_features

# Streamlit UI
st.set_page_config(page_title="Phish & Destroy", page_icon="🎣")

# Toggle dark/light theme (placeholder switch)
st.toggle("🌗 Dark Mode", value=False, key="theme_toggle")

st.markdown("""
    <h1 style='text-align: center;'>🎣 Phish & Destroy</h1>
    <p style='text-align: center;'>Your friendly AI tool to fight phishing and bad passwords.</p>
    <hr style='border: 1px solid #ddd;'>
""", unsafe_allow_html=True)

# Tab-based navigation
tab1, tab2 = st.tabs(["📧 Email Phishing Detector", "🔐 Password Checker"])

# === Phishing Detection Tab ===
with tab1:
    st.markdown("Enter email content and check if it's phishing or not.")

    if st.button("📋 Try Example Email"):
        st.session_state["example_email"] = "Dear user, your account has been suspended. Please click the link below to verify your account immediately. http://phishy.fake/login"
    else:
        st.session_state.setdefault("example_email", "")

    email_text = st.text_area("📝 Paste email content here:", height=250, value=st.session_state["example_email"])
    if st.button("🚨 Detect Phishing"):
        if email_text.strip() == "":
            st.warning("Please enter some email content.")
        else:
            try:
                # Call the updated extract_features function
                X_input = extract_features(email_text)
                prediction = model.predict(X_input)[0]

                if prediction == 1:
                    st.error("⚠️ This email looks like **Phishing**!")
                else:
                    st.success("✅ This email seems **Legitimate**.")
            except Exception as e:
                st.error(f"Error during prediction: {e}. Make sure model/vectorizer/scaler match input features.")
                st.exception(e) # This will print the full traceback for debugging

# === Password Checker Tab ===
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

# === Footer ===
st.markdown("""
---
<p style='text-align: center;'>Built with ❤️ by Alen using Streamlit, scikit-learn and Python 🐍</p>
""", unsafe_allow_html=True)
