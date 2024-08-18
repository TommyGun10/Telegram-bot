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


initiate_db()


for i in range(1, 5):
    add_product(f'Продукт {i}', f'Описание {i}', 100 * i, fr'C:\Users\User\Desktop\курсы\TelegramBot\Img\{i}.jpg')
