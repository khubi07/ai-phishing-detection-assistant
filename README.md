# AI Phishing Detection Assistant

An AI-powered phishing detection system that combines Machine Learning and Large Language Models (LLMs) to analyze emails, assess risk, explain threats, and generate reply suggestions.

## Overview

The application analyzes email content and provides:

* Phishing/Spam prediction
* Risk score assessment
* AI-generated email summary
* Threat explanation
* Suspicious indicator detection
* Reply recommendation for legitimate emails

Built to demonstrate the integration of NLP, Machine Learning, FastAPI, and Generative AI in a cybersecurity-focused application.

---

## Screenshots

### Main Interface

*Add screenshot here*

### Phishing Analysis Example

*Add screenshot here*

### Legitimate Email Analysis Example

*Add screenshot here*

---

## Live Demo

**Frontend:** *Add deployment link*

**Backend API Docs:** *Add deployment link*

---

## Architecture

```text
Email Input
    ↓
Streamlit Frontend
    ↓
FastAPI Backend
    ↓
TF-IDF + ML Classifier
    ↓
Groq LLM Analysis
    ↓
Risk Score + Summary + Explanation + Reply
```

---

## Dataset

### Primary Dataset

The deployed model was trained on the SMS Spam Collection dataset containing legitimate and spam messages.

| Metric  | Value               |
| ------- | ------------------- |
| Samples | 5,572               |
| Classes | Spam / Ham          |
| Type    | Text Classification |

### Dataset Experiments

Multiple phishing-oriented email datasets were evaluated during development.

Experiments included:

* Phishing email datasets
* Synthetic phishing corpora
* Multi-category phishing datasets containing:

  * Credential Harvesting
  * Financial Scams
  * Authority Scams
  * Social Engineering
  * Tech Support Scams

Several datasets produced near-perfect offline metrics but demonstrated poor real-world generalization during manual testing. These experiments informed the final model selection process.

---

## Model Evaluation

### Models Tested

| Model                        | Status    |
| ---------------------------- | --------- |
| Multinomial Naive Bayes      | Selected  |
| Logistic Regression          | Evaluated |
| Support Vector Machine (SVM) | Evaluated |

### Selection Criteria

Models were compared using:

* Accuracy
* Precision
* Recall
* F1 Score
* Manual phishing-email testing
* Real-world generalization behavior

The final model was selected based on overall performance and deployment suitability.

---


## Tech Stack

* Python
* Streamlit
* FastAPI
* Scikit-learn
* NLTK
* Groq API
* Pandas
* NumPy

---

## Performance

| Metric                   | Value    |
| ------------------------ | -------- |
| ML Prediction Latency    | ~9.6 ms  |
| End-to-End Analysis Time | ~2.3 sec |

The ML classifier performs inference in milliseconds, while most response time comes from LLM-powered analysis and explanation generation.

---

## Installation

```bash
git clone <repository-url>

cd <repository-name>

pip install -r requirements.txt

uvicorn api:app --reload

streamlit run app.py
```

---

## Disclaimer

This project is intended for educational and research purposes and should not be considered a replacement for enterprise-grade email security solutions.
