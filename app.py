from flask import Flask, render_template, url_for, request, redirect
import web_scraping

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/news', methods=['POST', 'GET'])
def news():
    key = request.form['key']

    #Toggle is opposite of what appears on screen
    if request.form.get('sentiment') == "on":
        sentiment = "off"
    else:
        sentiment = "on"

    if key == "Home":
        return redirect('/')
    articles = web_scraping.get_articles(key, sentiment)
    return render_template('news.html', articles=articles, sentiment=sentiment)

if __name__ == "__main__":
    app.run(debug=True)