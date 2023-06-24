import sqlite3


def create_database():
    database = sqlite3.connect('gazetauz.db')
    cursor = database.cursor()

    cursor.executescript('''
    DROP TABLE IF EXISTS info;
    DROP TABLE IF EXISTS categories;
    
    CREATE TABLE IF NOT EXISTS categories(
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name VARCHAR(20) UNIQUE,
        category_link TEXT UNIQUE
    );
    
    CREATE TABLE IF NOT EXISTS info(
        info_id INTEGER PRIMARY KEY AUTOINCREMENT,
        info_name TEXT UNIQUE,
        info_time TEXT,
        info_desc TEXT,
        info_link TEXT UNIQUE,
        category_id INTEGER REFERENCES categories(category_id)
    );
    ''')
    database.commit()
    database.close()
