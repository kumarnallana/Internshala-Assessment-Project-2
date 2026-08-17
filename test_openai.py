import os
from dotenv import load_dotenv
load_dotenv()

from app.classification.gemini_classifier import GeminiClassifier

classifier = GeminiClassifier()
batch = ['contact@singingbowlsexporter.com', 'contact@www.sacredsingingbowl.com', 'test@gmail.com']

print("OpenAI Key exists:", bool(classifier.openai_key))
print("Use mock:", classifier.use_mock)

results = classifier._classify_with_openai(batch)
print("Results:", results)
