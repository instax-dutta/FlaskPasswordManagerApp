from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from cryptography.fernet import Fernet
import hashlib

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('passwords.db')
    conn.row_factory = sqlite3.Row
    return conn

def load_key():
    return open("secret.key", "rb").read()

def encrypt_password(password):
    key = load_key()
    f = Fernet(key)
    encrypted_password = f.encrypt(password.encode())
    return encrypted_password

def decrypt_password(encrypted_password):
    key = load_key()
    f = Fernet(key)
    decrypted_password = f.decrypt(encrypted_password).decode()
    return decrypted_password

@app.route('/')
def index():
    conn = get_db_connection()
    passwords = conn.execute('SELECT * FROM passwords').fetchall()
    conn.close()
    return render_template('index.html', passwords=passwords, decrypt_password=decrypt_password)

@app.route('/add', methods=('GET', 'POST'))
def add():
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
    conn = get_db_connection()
    conn.execute('DELETE FROM passwords WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)