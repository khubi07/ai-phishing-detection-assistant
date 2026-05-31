import streamlit as st
import requests

st.title("AI Phishing Detection Assistant")
input_sms = st.text_area("Paste Email Content")
if st.button('Predict'):

    response = requests.post(
        "http://127.0.0.1:8000/analyze",
        json={
            "text": input_sms
        }
    )

    data = response.json()

    st.metric("Risk Score", f"{data['risk_score']}/100")

    st.metric(
        "Analysis Time",
        f"{data['latency']} sec"
    )

    st.metric(
        "ML Prediction Time",
        f"{data['ml_latency_ms']} ms"
    )

    st.subheader("Prediction")
    st.write(data["prediction"])

    st.subheader("AI Summary")
    st.write(data["summary"])

    st.subheader("Detected Indicators")
    st.write(data["indicators"])

    st.subheader("AI Risk Explanation")
    st.write(data["explanation"])

    

    prediction = data["prediction"]
    risk_score = data["risk_score"]

    if data["risk_score"] >= 70:

        st.warning("⚠️ Security Recommendation")

        st.write("""
        • Do not reply to this message.
        • Do not click suspicious links.
        • Do not share passwords or personal information.
        • Verify the sender independently.
        """)

    else:

        st.subheader("Suggested Reply")
        st.write(data["reply"])
        