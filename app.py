from flask import Flask, render_template, url_for, request
import web_scraping

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/news', methods=['POST', 'GET'])
def news():
    key = request.form['key']
    if key == "Home":
        return index()
    articles = web_scraping.get_articles(key)
    return render_template('news.html', articles=articles)

if __name__ == "__main__":
    app.run(debug=True)