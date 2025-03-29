from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from g4f.client import Client

app = Flask(__name__, static_url_path='')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)
client = Client()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/support')
def support():
    return render_template('support.html')

# Mock user database
users = {}

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'success': False, 'error': 'Email and password are required'}), 400
        
    if email in users and users[email]['password'] == password:
        return jsonify({'success': True, 'name': users[email]['name']})
    return jsonify({'success': False, 'error': 'Invalid email or password'}), 401

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'success': False, 'error': 'Email and password are required'}), 400
        
    if email in users:
        return jsonify({'success': False, 'error': 'Email already exists'}), 409
        
    users[email] = {"password": password}
    return jsonify({'success': True, 'name': email.split('@')[0]})

@app.route('/chatbot', methods=['POST'])
def chatbot():
    message = request.json.get('message')
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message}]
    )
    return jsonify({'response': response.choices[0].message.content})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
