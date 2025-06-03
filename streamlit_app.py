import streamlit as st
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Load the model and vectorizer
with open('phishing_detector_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open('tfidf_vectorizer.pkl', 'rb') as vec_file:
    vectorizer = pickle.load(vec_file)

# ---------- Feature Engineering Function ----------
def extract_features(email_text):
    email_length = len(email_text)
    num_exclamations = email_text.count('!')
    num_links = email_text.count('http') + email_text.count('www')
    num_uppercase_words = sum(1 for word in email_text.split() if word.isupper())
    num_special_chars = sum(not c.isalnum() and not c.isspace() for c in email_text)
    
    return pd.DataFrame([[
        email_length,
        num_exclamations,
        num_links,
        num_uppercase_words,
        num_special_chars
    ]], columns=['email_length', 'num_exclamations', 'num_links', 'num_uppercase_words', 'num_special_chars'])

# ---------- Streamlit UI ----------
st.set_page_config(page_title="Phish & Destroy", page_icon="🎣")
st.title("🎣 Phish & Destroy - Email Phishing Detector")
st.write("Enter the content of an email below, and we'll let you know if it's **phishing** or **legitimate**.")

# Text input
email_text = st.text_area("📧 Paste your email content here:", height=250)

if st.button("🔍 Check for Phishing"):
    if email_text.strip() == "":
        st.warning("Please enter some email content.")
    else:
        # TF-IDF transformation
        tfidf_features = vectorizer.transform([email_text])

        # Extract numeric features
        custom_features = extract_features(email_text)

        # Combine both
        from scipy.sparse import hstack
        final_input = hstack([tfidf_features, custom_features])

        # Predict
        prediction = model.predict(final_input)[0]

        if prediction == 1:
            st.error("⚠️ This email looks like **Phishing**!")
        else:
            st.success("✅ This email seems **Legitimate**.")

st.markdown("---")
st.caption("Built with ❤️ using Streamlit and scikit-learn")
