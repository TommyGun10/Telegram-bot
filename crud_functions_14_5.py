import sqlite3

def db_connection_decorator(func):
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('new_db.db')
        cursor = conn.cursor()

        result = func(cursor, *args, **kwargs)

        conn.commit()
        conn.close()
        return result
    return wrapper

@db_connection_decorator
def initiate_db(cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL,
    image_path TEXT NOT NULL)
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER NOT NULL,
    balance INTEGER NOT NULL DEFAULT 1000)
    ''')

@db_connection_decorator
def get_all_products(cursor):
    cursor.execute('''SELECT * FROM Products''')
    products = cursor.fetchall()
    return products

@db_connection_decorator
def add_product(cursor, title, description, price, image_path):
    cursor.execute('''
    INSERT INTO Products (title, description, price, image_path) VALUES (?, ?, ?, ?)
    ''', (title, description, price, image_path))

@db_connection_decorator
def add_user(cursor, username, email, age):
    cursor.execute('''
    INSERT INTO Users (username, email, age) VALUES (?, ?, ?)
    ''', (username, email, age))

@db_connection_decorator
def is_included(cursor, username):
    cursor.execute('''
    SELECT COUNT(*) FROM Users WHERE username = ?
    ''', (username,))
    count = cursor.fetchone()[0]
    return count > 0

initiate_db()


for i in range(1, 5):
    add_product(f'Продукт {i}', f'Описание {i}', 100 * i, fr'C:\Users\User\Desktop\курсы\TelegramBot\Img\{i}.jpg')


add_user('user1', 'user1@example.com', 25)
add_user('user2', 'user2@example.com', 30)

