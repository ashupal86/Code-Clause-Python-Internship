from flask import Flask,render_template
from scrapper import news

app = Flask(__name__,template_folder='templates',static_folder='static',static_url_path='/static')

@app.route('/')
def home():
    news_dict=news()
    headlines=[(headline, link) for headline, link in news_dict.items()]

    return render_template('index.html',news=headlines)



if __name__ == '__main__':
    app.run(debug=True)
