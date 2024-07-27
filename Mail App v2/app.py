import os
import base64
import sqlite3
from email.mime.text import MIMEText
from flask import Flask, redirect, url_for, session, request, render_template
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Set the environment variable to allow HTTP for OAuth 2.0 during development
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Replace these with your OAuth2 client credentials
# CLIENT_SECRETS_FILE = 'credentials.json'
CLIENT_SECRETS_FILE = os.getenv('credentials')


# Define the required OAuth2.0 scopes
SCOPES = [
     'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'openid'
]

API_SERVICE_NAME = 'gmail'
API_VERSION = 'v1'

# Set up SQLite database
DATABASE = 'emails.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS emails
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         sender TEXT,
                         recipient TEXT,
                         subject TEXT,
                         message TEXT,
                     timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')

@app.route('/')
def index():
    if 'credentials' not in session:
        return redirect('authorize')
    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()
        cur.execute("SELECT sender, recipient, subject, message, timestamp FROM emails")
        emails = cur.fetchall()
    return render_template('index.html', emails=list(reversed(emails)))

@app.route('/authorize')
def authorize():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)
    flow.redirect_uri = url_for('authenticate', _external=True)

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')

    session['state'] = state

    return redirect(authorization_url)

@app.route('/authenticate')
def authenticate():
    state = session['state']
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = url_for('authenticate', _external=True)

    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)

    # Fetch the user's profile information
    user_info = get_user_info(credentials)
    user_email = user_info.get('email')
    user_name = user_info.get('name')
    session['user_email'] = user_email
    session['user_name'] = user_name

    return redirect(url_for('index'))

@app.route('/send_email', methods=['POST'])
def send_email():
    if 'credentials' not in session:
        return redirect('authorize')

    credentials = Credentials(**session['credentials'])

    service = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

    sender = session.get('user_email')  # Use authenticated user's email as sender
    to = request.form['to']
    subject = request.form['subject']
    message_text = request.form['message']

    message = create_message(sender, to, subject, message_text)
    send_message(service, 'me', message)

    # Store the sent email in the database
    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO emails (sender, recipient, subject, message) VALUES (?, ?, ?, ?)",
                    (sender, to, subject, message_text))
        conn.commit()

    return 'Email sent!'

def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw_message}

def send_message(service, user_id, message):
    try:
        message = service.users().messages().send(userId=user_id, body=message).execute()
        print(f'Message Id: {message["id"]}')
        return message
    except Exception as error:
        print(f'An error occurred: {error}')
        return None

def get_user_info(credentials):
    user_info_service = build('oauth2', 'v2', credentials=credentials)
    user_info = user_info_service.userinfo().get().execute()
    return user_info

def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
