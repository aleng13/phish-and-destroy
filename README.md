# Phishing Email Detector using AI/ML

[![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
# Phish & Destroy

**Phish & Destroy** is a machine learning-powered web application designed to detect phishing emails and assess password strength. It is built using `scikit-learn`, `Streamlit`, and deployed on Streamlit Cloud.

Check it out on --> https://phish-and-destroy.streamlit.app/
---

## 🔍 Project Overview

Phishing is a deceptive tactic used by attackers to trick users into revealing sensitive information via fake emails or messages. This tool helps identify such emails and offers guidance on creating stronger passwords.

**Key Features:**
- Phishing email detection via ML
- Password strength analyzer
- Clean, interactive UI built with Streamlit

---

## 📁 Dataset

The dataset is sourced from [Kaggle - Phishing Email Dataset](https://www.kaggle.com/datasets/naserabdullahalam/phishing-email-dataset), and contains:

- `text_combined`: Raw email content
- `label`: 1 for phishing, 0 for legitimate

---

## ⚙️ Feature Engineering

### 1. TF-IDF Vectorization
- Converts email text into numerical vectors based on term frequency and inverse document frequency.

### 2. Extended Feature Set (Used in Final Model)
Alongside TF-IDF, we engineered these custom features:
- Total email length
- Number of exclamation marks (`!`)
- Count of suspicious links (`http`, `www`)
- Number of fully uppercase words
- Count of special characters

These features were scaled using `StandardScaler` and horizontally stacked with the TF-IDF vector using `scipy.sparse.hstack`.

---

## 🧠 Model Training and Evaluation

Two models were trained and evaluated:

| Model               | Accuracy | Precision | Recall | F1 Score |
|--------------------|----------|-----------|--------|----------|
| **Logistic Regression** (Final Model) | **98%**   | 98%       | 99%    | 98%      |
| Naive Bayes         | 97%      | 96%       | 97%    | 96%      |

- **Logistic Regression** performed slightly better and was selected for deployment.
- Confusion matrices and classification reports are included in the repo.
---

## 🔐 Password Strength Checker

This tool evaluates passwords based on:

- Minimum length (8 characters)
- Presence of uppercase and lowercase characters
- At least one digit
- At least one special character
- Not in a list of common weak passwords

### Scoring:
- **Strong** → 100%
- **Moderate** → 60–80%
- **Weak** → Below 60%

Tips are provided dynamically to help users improve weak passwords.

---

## 🖥️ Streamlit App Features

The interface includes two primary tabs:

### 📧 Email Phishing Detector
- Paste or test with an example email.
- Uses trained ML model to predict phishing.
- Includes a reset (clear) button.

### 🔐 Password Strength Analyzer
- Input password to check its strength.
- Dynamic suggestions and progress bar.

---

## 🚀 Deployment

The app is deployed on https://phish-and-destroy.streamlit.app/

To deploy it yourself:
1. Push the following files to GitHub:
   - `streamlit_app.py`
   - `phishing_detector_model_enhanced.pkl`
   - `tfidf_vectorizer_enhanced.pkl`
   - `feature_scaler_enhanced.pkl`
   - `requirements.txt`
2. Github: https://github.com/aleng13/phish-and-destroy/tree/main
3. Click **Deploy**.

---
## 👨‍💻 Author

**Alen George Scaria**

This project was built to explore and understand the complete ML pipeline:
- Data preprocessing
- Feature engineering
- Model training and evaluation
- Real-world deployment

Feel free to connect:
- LinkedIn: https://www.linkedin.com/in/alen-georg013/
- GitHub: https://github.com/aleng13

---
