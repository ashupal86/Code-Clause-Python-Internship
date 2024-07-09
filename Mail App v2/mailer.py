import sqlite3
def init_db(DATABASE):
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS emails
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         sender TEXT,
                         recipient TEXT,
                         subject TEXT,
                         message TEXT)''')
        
def list_emails(DATABASE):
    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()
        cur.execute("SELECT sender, recipient, subject, message FROM emails")
        emails = cur.fetchall()
    return emails

def add_email(DATABASE, sender, recipient, subject, message):
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("INSERT INTO emails (sender, recipient, subject, message) VALUES (?, ?, ?, ?)",
                     (sender, recipient, subject, message))


# def create_email( sender, recipient, subject, message):  
