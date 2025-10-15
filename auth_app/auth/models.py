import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect('instance/app.db')
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database and create tables"""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


class User:
    def __init__(self, id=None, email=None, password_hash=None, created_at=None):
        self.id = id
        self.email = email
        self.password_hash = password_hash
        self.created_at = created_at

    def set_password(self, password: str) -> None:
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Check if password matches hash"""
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_email(email: str):
        """Get user by email"""
        conn = get_db_connection()
        user_row = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()
        
        if user_row:
            return User(
                id=user_row['id'],
                email=user_row['email'],
                password_hash=user_row['password_hash'],
                created_at=user_row['created_at']
            )
        return None

    @staticmethod
    def get_by_id(user_id: int):
        """Get user by ID"""
        conn = get_db_connection()
        user_row = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        conn.close()
        
        if user_row:
            return User(
                id=user_row['id'],
                email=user_row['email'],
                password_hash=user_row['password_hash'],
                created_at=user_row['created_at']
            )
        return None

    def save(self):
        """Save user to database"""
        conn = get_db_connection()
        if self.id is None:
            # Insert new user
            cursor = conn.execute(
                'INSERT INTO users (email, password_hash) VALUES (?, ?)',
                (self.email, self.password_hash)
            )
            self.id = cursor.lastrowid
            conn.commit()
        else:
            # Update existing user
            conn.execute(
                'UPDATE users SET email = ?, password_hash = ? WHERE id = ?',
                (self.email, self.password_hash, self.id)
            )
            conn.commit()
        conn.close()
