from transformers import pipeline
summarizer = pipeline("summarization")
def get_abstract_summary(text):
    s = summarizer(text, min_length=5, max_length=100)
    print(s)
    return s[0]['summary_text']
