from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from functools import wraps

from .models import User


auth_bp = Blueprint('auth', __name__, template_folder='../templates')


def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Пожалуйста, войдите в систему', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def get_current_user():
    """Get current logged in user"""
    if 'user_id' in session:
        return User.get_by_id(session['user_id'])
    return None


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    current_user = get_current_user()
    if current_user:
        return redirect(url_for('auth.profile'))

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

        existing = User.get_by_email(email)
        if existing:
            flash('Пользователь с таким email уже существует', 'warning')
            return render_template('register.html')

        user = User(email=email)
        user.set_password(password)
        user.save()

        flash('Регистрация успешна! Войдите в систему.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    current_user = get_current_user()
    if current_user:
        return redirect(url_for('auth.profile'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        user = User.get_by_email(email)
        if not user or not user.check_password(password):
            flash('Неверный email или пароль', 'danger')
            return render_template('login.html')

        session['user_id'] = user.id
        flash('Вы вошли в систему', 'success')
        next_url = request.args.get('next')
        return redirect(next_url or url_for('auth.profile'))

    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/profile')
@login_required
def profile():
    current_user = get_current_user()
    return render_template('profile.html', email=current_user.email)
