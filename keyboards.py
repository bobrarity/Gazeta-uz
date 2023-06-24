from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
import sqlite3

database = sqlite3.connect('gazetauz.db')
cursor = database.cursor()

cursor.execute('''
SELECT category_name FROM categories;
''')
CATEGORIES = cursor.fetchall()


def generate_buttons():
    markup = ReplyKeyboardMarkup()
    buttons = []
    for i in CATEGORIES:
        btn = KeyboardButton(text=i[0])
        buttons.append(btn)
    markup.add(*buttons)
    return markup
