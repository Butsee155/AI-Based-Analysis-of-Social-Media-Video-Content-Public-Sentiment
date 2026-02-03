from flask import Flask, request, jsonify
import joblib
import pandas as pd
import re

app = Flask(__name__)

# Load trained model + vectorizer
model = joblib.load('model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

def clean_text(text):
    text = text.lower()
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d', '', text)
    return text

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    news_text = data.get('text', '')
    clean = clean_text(news_text)
    vector = vectorizer.transform([clean])
    prediction = model.predict(vector)[0]
    label = "🟢 Real News" if prediction == 1 else "🔴 Fake News"
    return jsonify({'result': label})

if __name__ == '__main__':
    app.run(debug=True)
