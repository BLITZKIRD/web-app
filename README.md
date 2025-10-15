Flask Authentication App

Приложение для аутентификации и авторизации пользователей на чистом Flask (без дополнительных расширений).

## Особенности

- Использует только Flask (без Flask-SQLAlchemy, Flask-Login и других расширений)
- Нативная работа с SQLite через sqlite3
- Сессионная аутентификация
- Хеширование паролей через Werkzeug (встроено в Flask)
- Регистрация и вход пользователей
- Защищенные маршруты

## Установка и запуск

```bash
# Клонировать репозиторий
git clone https://github.com/your-username/flask-auth-app.git

cd flask-auth-app

# Установить зависимости
pip install -r auth_app/requirements.txt

# Запустить приложение
python -m auth_app.app
```

Перейдите по адресу: http://localhost:5000

## Использование

1. Перейдите на `/register` для регистрации нового пользователя
2. Войдите в систему на `/login`
3. Просмотрите профиль на `/profile`
4. Выйдите из системы через `/logout`

## Структура

```
auth_app/
├── app.py              # Главное Flask приложение
├── auth/
│   ├── models.py      # Модели пользователей (sqlite3)
│   └── routes.py      # Маршруты аутентификации
├── templates/         # HTML шаблоны
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   └── profile.html
├── requirements.txt   # Зависимости (только Flask)
└── __init__.py
```

## Технологии

- **Flask 3.0.3** - веб-фреймворк
- **SQLite** - база данных (нативный sqlite3)
- **Werkzeug** - хеширование паролей (встроено в Flask)
- **Sessions** - аутентификация пользователей
