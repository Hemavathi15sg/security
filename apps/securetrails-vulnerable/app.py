# app.py - SecureTrails Backend
# INTENTIONAL VULNERABILITIES FOR WORKSHOP

from flask import Flask, render_template, request, session, jsonify, redirect
import sqlite3
import os
from hashlib import md5
from datetime import datetime
import json

app = Flask(__name__)

# VULNERABILITY 1: Hardcoded JWT Secret
app.secret_key = 'super-secret-key-12345'
JWT_SECRET = 'super-secret-key-12345'

# VULNERABILITY 2: CORS Misconfiguration
from flask_cors import CORS
CORS(app, origins="*")  # Allows all origins

# Database connection with hardcoded path
DATABASE = 'database.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

# VULNERABILITY 3: SQL Injection in login
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # SQL INJECTION - User input directly in query
    db = get_db()
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{md5(password.encode()).hexdigest()}'"
    
    try:
        user = db.execute(query).fetchone()
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect('/dashboard')
        else:
            return render_template('login.html', error='Invalid credentials')
    except Exception as e:
        return render_template('login.html', error='Database error')

# VULNERABILITY 4: Broken Authentication - Missing Session Validation
@app.route('/admin')
def admin():
    # No proper session validation
    if request.args.get('user_id'):
        user_id = request.args.get('user_id')
        # Missing validation - any user can access any admin panel
        return render_template('admin.html', user_id=user_id)
    return redirect('/login')

# VULNERABILITY 5: Insecure Direct Object Reference (IDOR)
@app.route('/trail/<trail_id>')
def view_trail(trail_id):
    # No authorization check - anyone can view any trail
    db = get_db()
    # SQL INJECTION VARIANT
    query = f"SELECT * FROM trails WHERE id = {trail_id}"
    
    trail = db.execute(query).fetchone()
    if trail:
        return render_template('trails.html', trail=dict(trail))
    return 'Trail not found', 404

# VULNERABILITY 6: Weak Password Hashing (MD5)
def hash_password(password):
    # MD5 is broken for password hashing
    return md5(password.encode()).hexdigest()

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Weak hash
    hashed = hash_password(password)
    
    db = get_db()
    db.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
               (username, hashed))
    db.commit()
    return 'User registered'

# VULNERABILITY 7: Sensitive Data Exposure - Debug Mode
DEBUG = True  # Debug mode exposes sensitive information

if DEBUG:
    @app.route('/debug')
    def debug_info():
        return jsonify({
            'secret_key': app.secret_key,
            'jwt_secret': JWT_SECRET,
            'database': DATABASE,
            'debug': DEBUG
        })

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    
    db = get_db()
    trails = db.execute("SELECT * FROM trails").fetchall()
    return render_template('trails.html', trails=trails)

@app.route('/trails', methods=['GET'])
def get_trails():
    db = get_db()
    trails = db.execute("SELECT * FROM trails").fetchall()
    return jsonify([dict(trail) for trail in trails])

@app.route('/comments/<trail_id>', methods=['POST'])
def post_comment(trail_id):
    comment = request.form.get('comment')
    
    # Comment stored and rendered without escaping
    db = get_db()
    db.execute("INSERT INTO trail_comments (trail_id, comment, created_at) VALUES (?, ?, ?)",
               (trail_id, comment, datetime.now()))
    db.commit()
    
    return 'Comment posted'

@app.route('/search')
def search():
    q = request.args.get('q', '')
    # SQL INJECTION IN SEARCH
    query = f"SELECT * FROM trails WHERE name LIKE '%{q}%' OR description LIKE '%{q}%'"
    
    db = get_db()
    results = db.execute(query).fetchall()
    return render_template('trails.html', trails=results, search_query=q)

if __name__ == '__main__':
    app.run(debug=DEBUG)
