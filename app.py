from flask import Flask, request, redirect, jsonify

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

#/abstract_summary?text=ASDASDAD
@app.route("/abstract_summary", methods=['GET'])
def abstract_summary():
    data = request.args
    text = data.get('text') 
    from abstract import get_abstract_summary
    summary = get_abstract_summary(text)
    dic = {"text": text, "summary":summary}

    return jsonify(dic)

@app.route("/sentiment", methods=['GET'])
def sentiment():
    from sentiment import get_sentiment
    data = request.args
    text = data.get('text')
    dic = get_sentiment(text)
    dic['text'] = text

    return jsonify(dic)

@app.route("/extract_summary", methods=['GET'])
def extract_summary():
    from extraction_textrank import generate_extract_summary
    data = request.args
    text = data.get('text') 

    summary = generate_extract_summary(text, False)
    dic = {"text": text, "summary":summary}

    return jsonify(dic)

@app.route("/youtubeToText", methods=['GET'])
def youtubize():
    from linkToText import get_text
    data = request.args
    url = data.get('url')
    text = get_text(url)
    dic = {"url": url, "transcript": text}
    return jsonify(dic)

@app.route("/")
def index():
    return redirect("http://yoonpatrick3.github.io")

if __name__ == '__main__':
    app.run(debug=True)