# Mail App
This project is a Flask-based web application that allows users to send emails using the Gmail API. It provides a simple interface to compose and send emails, fetches and displays a list of sent emails, and allows viewing details of each email.

## Table of Contents
- [Mail App](#mail-app)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Project Structure Mail App](#project-structure-mail-app)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Libraries Used](#libraries-used)
  - [Contributing](#contributing)




## Features
- **Compose Email:** Users can fill out a form to send emails.
- **View Sent Emails:** Displays a list of sent emails with basic details.
- **View Email Details:** Allows users to click on an email to view its details (recipient, subject, message).
- **OAuth2 Authentication:** Integration with Gmail API using OAuth2 for secure authentication and authorization.
- **SQLite Database:** Stores sent emails for future reference.
- **Responsive Design:** Basic styling using custom CSS for a clean and responsive user interface.

## Project Structure Mail App 
```
│
├── app.py            # Main Flask application file
├── credentials.json  # Client secrets for OAuth 2.0 authentication
├── emails.db         # SQLite database for storing emails
├── static/
│   ├── scripts.js    # JavaScript for client-side interactions
│   └── styles.css    # CSS for styling the web interface
│
└── templates/
    └──index.html    # HTML template for the web interface
    

```
## Installation
To run this project locally, follow these steps:

1. **Clone Repository:**
   ```bash
   git clone https://github.com/ashupal86/Code-Clause-Python-Internship/tree/main/Mail%20App%20v2
   cd mail-app
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up OAuth2 Credentials:**
   - Obtain OAuth2 client credentials from Google Developer Console.
   - Download `credentials.json` and place it in the root directory of the project.

4. **Run the Application:**
   ```bash
   python app.py
   ```
   Open your web browser and navigate to `http://localhost:5000` OR `http://127.0.0.1:5000` to access the application.

## Usage
- **Sending Emails:** Click on "Send Email", fill out the form, and click "Send".
- **Viewing Sent Emails:** Sent emails are listed on the left. Click on an email to view details on the right.
- **OAuth2 Authentication:** On the first run, you'll be prompted to authorize the app to access your Gmail account.

## Libraries Used
- **Flask:** Web framework for Python.
- **SQLite:** Embedded SQL database engine.
- **Google API Client Libraries:** Integration with Gmail API for sending emails.
- **OAuthlib:** OAuth2 integration for secure authentication.

## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your improvements.

