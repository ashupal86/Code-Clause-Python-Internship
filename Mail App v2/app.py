from flask import Flask, redirect, url_for, session, request, render_template
from mailer import init_db

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'


@app.route('/')
def index():
    if 'credentials' not in session:
        return redirect('authorize')
    return render_template('index.html')

@app.route('/authorize')
def authorize():
    return 'You are authorized to send emails!'

@app.route('/authenticate')
def authenticate():
    return 'You are authorized to send emails!'

if __name__ == '__main__':
    init_db("emails.db")
    app.run(debug=True)
