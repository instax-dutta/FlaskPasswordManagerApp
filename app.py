from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
import os
import random
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from base64 import urlsafe_b64encode
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

def get_db_connection():
    conn = sqlite3.connect('passwords.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    with conn:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            website TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
        ''')
    conn.close()

def generate_passphrase(num_words=4):
    wordlist = [
        'apple', 'banana', 'cherry', 'date', 'elderberry', 'fig', 'grape', 'honeydew',
        'kiwi', 'lemon', 'mango', 'nectarine', 'orange', 'papaya', 'quince', 'raspberry',
        'strawberry', 'tangerine', 'ugli', 'vanilla', 'watermelon', 'xigua', 'yam', 'zucchini'
    ]
    passphrase = ' '.join(random.sample(wordlist, num_words))
    return passphrase

def generate_salt(length=16):
    return base64.urlsafe_b64encode(os.urandom(length)).decode()

def save_passphrase_and_salt(passphrase, salt, filepath='passphrase.txt'):
    with open(filepath, 'w') as f:
        f.write(f'{passphrase}\n{salt}')

def load_passphrase_and_salt(filepath='passphrase.txt'):
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            lines = f.readlines()
            return lines[0].strip(), lines[1].strip()
    return None, None

def derive_key_from_passphrase(passphrase, salt):
    backend = default_backend()
    salt = base64.urlsafe_b64decode(salt.encode())
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=backend
    )
    key = urlsafe_b64encode(kdf.derive(passphrase.encode()))
    return key

# Initialize the database
init_db()

# Generate and save the passphrase and salt if they don't exist
passphrase, salt = load_passphrase_and_salt()
if passphrase is None or salt is None:
    passphrase = generate_passphrase()
    salt = generate_salt()
    save_passphrase_and_salt(passphrase, salt)
    print(f'Generated passphrase: {passphrase}')
    print(f'Generated salt: {salt}')
else:
    print(f'Loaded passphrase: {passphrase}')
    print(f'Loaded salt: {salt}')

def encrypt_password(password):
    key = derive_key_from_passphrase(passphrase, salt)
    f = Fernet(key)
    encrypted_password = f.encrypt(password.encode())
    return encrypted_password

def decrypt_password(encrypted_password):
    key = derive_key_from_passphrase(passphrase, salt)
    f = Fernet(key)
    decrypted_password = f.decrypt(encrypted_password).decode()
    return decrypted_password

@app.route('/')
def index():
    if 'authenticated' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    passwords = conn.execute('SELECT * FROM passwords').fetchall()
    conn.close()
    return render_template('index.html', passwords=passwords, decrypt_password=decrypt_password)

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        entered_passphrase = request.form['passphrase']
        if entered_passphrase == passphrase:
            session['authenticated'] = True
            return redirect(url_for('index'))
        else:
            flash('Incorrect passphrase. Please try again.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('login'))

@app.route('/validate_passphrase', methods=['POST'])
def validate_passphrase():
    data = request.get_json()
    entered_passphrase = data.get('passphrase')
    if entered_passphrase == passphrase:
        return jsonify(valid=True)
    else:
        return jsonify(valid=False)

@app.route('/add', methods=('GET', 'POST'))
def add():
    if 'authenticated' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        website = request.form['website']
        username = request.form['username']
        password = request.form['password']
        
        encrypted_password = encrypt_password(password)
        
        conn = get_db_connection()
        conn.execute('INSERT INTO passwords (website, username, password) VALUES (?, ?, ?)',
                     (website, username, encrypted_password))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    if 'authenticated' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    password = conn.execute('SELECT * FROM passwords WHERE id = ?', (id,)).fetchone()
    
    if request.method == 'POST':
        website = request.form['website']
        username = request.form['username']
        new_password = request.form['password']
        
        encrypted_password = encrypt_password(new_password)
        
        conn.execute('UPDATE passwords SET website = ?, username = ?, password = ? WHERE id = ?',
                     (website, username, encrypted_password, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    return render_template('edit.html', password=password, decrypt_password=decrypt_password)

@app.route('/delete/<int:id>')
def delete(id):
    if 'authenticated' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    conn.execute('DELETE FROM passwords WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=7777)
