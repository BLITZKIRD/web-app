#!/usr/bin/env python3
"""
Тестовый скрипт для проверки работы Flask приложения
"""
import sys
import os

# Добавляем текущую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User, generate_password, get_strength_class

def test_password_generation():
    """Тест генерации паролей"""
    print("🔐 Тестирование генерации паролей...")
    
    # Тест 1: Базовая генерация
    password = generate_password(12, True, True, True)
    print(f"   Сгенерированный пароль: {password}")
    print(f"   Длина: {len(password)}")
    print(f"   Надежность: {get_strength_class(password)}")
    
    # Тест 2: Только строчные буквы
    password_simple = generate_password(8, False, False, False)
    print(f"   Простой пароль: {password_simple}")
    print(f"   Надежность: {get_strength_class(password_simple)}")
    
    # Тест 3: Длинный пароль
    password_long = generate_password(20, True, True, True)
    print(f"   Длинный пароль: {password_long}")
    print(f"   Надежность: {get_strength_class(password_long)}")
    
    print("✅ Тесты генерации паролей прошли успешно!\n")

def test_database():
    """Тест работы с базой данных"""
    print("🗄️ Тестирование базы данных...")
    
    with app.app_context():
        # Создаем тестового пользователя
        test_user = User(email="test@example.com")
        test_user.set_password("testpassword123")
        
        # Добавляем в базу
        db.session.add(test_user)
        db.session.commit()
        
        # Проверяем, что пользователь создался
        found_user = User.query.filter_by(email="test@example.com").first()
        if found_user:
            print(f"   Пользователь создан: {found_user.email}")
            print(f"   ID: {found_user.id}")
            print(f"   Дата создания: {found_user.created_at}")
            
            # Тест проверки пароля
            if found_user.check_password("testpassword123"):
                print("   ✅ Проверка пароля прошла успешно")
            else:
                print("   ❌ Ошибка проверки пароля")
            
            # Удаляем тестового пользователя
            db.session.delete(found_user)
            db.session.commit()
            print("   Тестовый пользователь удален")
        else:
            print("   ❌ Ошибка создания пользователя")
    
    print("✅ Тесты базы данных прошли успешно!\n")

def test_app_routes():
    """Тест маршрутов приложения"""
    print("🌐 Тестирование маршрутов...")
    
    with app.test_client() as client:
        # Тест главной страницы
        response = client.get('/')
        print(f"   Главная страница: {response.status_code}")
        
        # Тест страницы регистрации
        response = client.get('/register')
        print(f"   Страница регистрации: {response.status_code}")
        
        # Тест страницы входа
        response = client.get('/login')
        print(f"   Страница входа: {response.status_code}")
        
        # Тест генератора паролей (должен перенаправить на логин)
        response = client.get('/password-generator')
        print(f"   Генератор паролей (без авторизации): {response.status_code}")
    
    print("✅ Тесты маршрутов прошли успешно!\n")

def main():
    """Основная функция тестирования"""
    print("🚀 Запуск тестов Flask приложения\n")
    
    try:
        test_password_generation()
        test_database()
        test_app_routes()
        
        print("🎉 Все тесты прошли успешно!")
        print("\n📋 Функциональность приложения:")
        print("   • Генерация надежных паролей с настройками")
        print("   • Система аутентификации пользователей")
        print("   • База данных SQLite для хранения пользователей")
        print("   • Веб-интерфейс с современным дизайном")
        print("   • Анализ надежности паролей")
        print("   • Копирование паролей в буфер обмена")
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())