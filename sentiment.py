from transformers import pipeline

nlp = pipeline("sentiment-analysis")

def get_sentiment(text):
    return nlp(text)[0]