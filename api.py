import string
import nltk
import pickle

# downloads
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')

from fastapi import FastAPI
from pydantic import BaseModel
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

ps = PorterStemmer()

import os

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# model loading
tfidf = pickle.load(open('vectorizer.pkl','rb'))
model = pickle.load(open('model.pkl','rb'))

# app creation
app = FastAPI()

# helper functions
def transform_text(text):
    #1. converted to lower
    text = text.lower()

    #2. tokenize the words and return list
    text = nltk.word_tokenize(text) 
    # we can run a loop on list to remove special char

    #3. removed special char
    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    #4. removed stopwords and punctuation
    text = y[:]
    y.clear()
    
    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    #5. stemming
    text = y[:]
    y.clear()
    for i in text:
        y.append(ps.stem(i))
    return " ".join(y)

def generate_summary(text):

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": f"Summarize this email in 2-3 concise bullet points:\n\n{text}"
            }
        ]
    )

    return response.choices[0].message.content

def explain_risk(text, prediction, risk_score):

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": f"""
Analyze this message.

Prediction: {prediction}
Risk Score: {risk_score}/100

Message:
{text}

Explain in 3-5 bullet points why this message may be suspicious or safe.
Focus on urgency, links, rewards, credential requests, threats, or other indicators.
"""
            }
        ]
    )

    return response.choices[0].message.content

def detect_indicators(text):

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": f"""
Analyze this email:

{text}

Return only a bullet list of suspicious indicators found.

Possible indicators:
- Urgent Language
- Suspicious Link
- Credential Request
- Financial Request
- Threat Language
- Unknown Sender
- Reward/Prize Offer
- Attachment Request

Return only the detected indicators.
"""
            }
        ]
    )

    return response.choices[0].message.content

def generate_reply(text):

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": f"""
Generate a professional and concise reply to this email:

{text}

Reply only with the email response.
"""
            }
        ]
    )

    return response.choices[0].message.content

# request schemas
class EmailRequest(BaseModel):
    text: str

# endpoints
@app.post("/predict")
def predict(request: EmailRequest):

    transformed_text = transform_text(request.text)

    vector_input = tfidf.transform([transformed_text])

    result = model.predict(vector_input)[0]

    prob = model.predict_proba(vector_input)

    spam_probability = prob[0][1]

    risk_score = round(spam_probability * 100)

    prediction = "spam" if result == 1 else "not spam"

    return {
        "prediction": prediction,
        "risk_score": risk_score
    }

@app.post("/analyze")
def analyze(request: EmailRequest):

    transformed_text = transform_text(request.text)

    vector_input = tfidf.transform([transformed_text])

    result = model.predict(vector_input)[0]

    prob = model.predict_proba(vector_input)

    spam_probability = prob[0][1]

    risk_score = round(spam_probability * 100)

    prediction = "spam" if result == 1 else "not spam"

    summary = generate_summary(request.text)

    explanation = explain_risk(
        request.text,
        prediction,
        risk_score
    )

    indicators = detect_indicators(request.text)

    reply = None

    if risk_score < 70:
        reply = generate_reply(request.text)

    return {
    "prediction": prediction,
    "risk_score": risk_score,
    "summary": summary,
    "explanation": explanation,
    "indicators": indicators,
    "reply": reply
}