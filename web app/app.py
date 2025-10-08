from flask import Flask, render_template, request
import random
import string
import re

app = Flask(__name__)

def generate_password(length=12, use_uppercase=True, use_numbers=True, use_special=True):
    characters = string.ascii_lowercase
    
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_numbers:
        characters += string.digits
    if use_special:
        characters += string.punctuation
    
    if not characters:
        characters = string.ascii_lowercase
    
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def get_strength_class(password):
    if not password:
        return "weak"
    
    strength = 0
    if len(password) >= 8:
        strength += 1
    if len(password) >= 12:
        strength += 1
    if re.search(r'[A-Z]', password):
        strength += 1
    if re.search(r'[0-9]', password):
        strength += 1
    if re.search(r'[^A-Za-z0-9]', password):
        strength += 1
    
    if strength >= 4:
        return "very-strong"
    elif strength >= 3:
        return "strong"
    elif strength >= 2:
        return "medium"
    else:
        return "weak"

@app.route('/', methods=['GET', 'POST'])
def index():
    password = ""
    length = 12
    uppercase = True
    numbers = True
    special = True
    
    if request.method == 'POST':
        length = int(request.form.get('length', 12))
        uppercase = 'uppercase' in request.form
        numbers = 'numbers' in request.form
        special = 'special' in request.form
        
        password = generate_password(length, uppercase, numbers, special)
    
    return render_template('index.html', 
                         password=password,
                         length=length,
                         uppercase=uppercase,
                         numbers=numbers,
                         special=special,
                         get_strength_class=get_strength_class)

if __name__ == '__main__':
    app.run(debug=True)