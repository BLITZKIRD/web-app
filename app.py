from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import random
import string
import re

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Пожалуйста, войдите в систему для доступа к этой странице.'
login_manager.login_message_category = 'info'


# User Model
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id: str):
    return User.query.get(int(user_id))


# Password Generator Functions
def generate_password(length=12, use_uppercase=True, use_numbers=True, use_special=True):
    """Generate a random password with specified criteria."""
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
    """Determine password strength class for styling."""
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


# Routes
@app.route('/')
def home():
    """Home page with password generator."""
    return redirect(url_for('password_generator'))


@app.route('/generator', methods=['GET', 'POST'])
@login_required
def password_generator():
    """Password generator page (requires login)."""
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
        flash('Пароль успешно сгенерирован!', 'success')
    
    return render_template('generator.html', 
                         password=password,
                         length=length,
                         uppercase=uppercase,
                         numbers=numbers,
                         special=special,
                         get_strength_class=get_strength_class)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration."""
    if current_user.is_authenticated:
        return redirect(url_for('password_generator'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm', '')
        
        if not email or not password:
            flash('Заполните email и пароль', 'danger')
            return render_template('register.html')
        
        if password != confirm:
            flash('Пароли не совпадают', 'danger')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Пароль должен содержать минимум 6 символов', 'danger')
            return render_template('register.html')
        
        existing = User.query.filter_by(email=email).first()
        if existing:
            flash('Пользователь с таким email уже существует', 'warning')
            return render_template('register.html')
        
        user = User(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Регистрация успешна! Войдите в систему.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login."""
    if current_user.is_authenticated:
        return redirect(url_for('password_generator'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            flash('Неверный email или пароль', 'danger')
            return render_template('login.html')
        
        login_user(user)
        flash('Добро пожаловать!', 'success')
        next_url = request.args.get('next')
        return redirect(next_url or url_for('password_generator'))
    
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    """User logout."""
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('login'))


@app.route('/profile')
@login_required
def profile():
    """User profile page."""
    return render_template('profile.html', user=current_user)


# Create database tables
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)