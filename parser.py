import requests
from bs4 import BeautifulSoup
import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('URL')
host = os.getenv('HOST')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'}


class CategoryParser:
    def __init__(self, url, name, category_id):
        self.url = url
        self.name = name
        self.category_id = category_id

    def get_html(self):
        html = requests.get(self.url, headers=headers).text
        return html

    def get_soup(self):
        html = self.get_html()
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    def get_data(self):
        soup = self.get_soup()
        articles = soup.find_all('div', class_='nblock')
        for article in articles:
            a_title = article.find('div', class_='nt').find('h3').get_text(strip=True)
            a_description = article.find('div', class_='nt').find('p').get_text(strip=True)
            a_time = article.find('div', class_='nt').find('div', class_='ndt').get_text(strip=True)
            a_link = host + article.find('a').get('href')
            # print(a_title)
            # print(a_time)
            # print(a_description)
            # print(a_link)
            database = sqlite3.connect('gazetauz.db')
            cursor = database.cursor()
            cursor.execute('''
            INSERT OR IGNORE INTO info(info_name, info_time, info_desc, info_link, category_id) VALUES(?, ?, ?, ?, ?)
            ''', (a_title, a_time, a_description, a_link, self.category_id))
            database.commit()
            database.close()


def parsing():
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'html.parser')
    blocks = soup.find('ul', class_='nav__container-items').find_all('li')
    for block in blocks:
        category_link = host + block.find('a').get('href')
        category_name = block.find('a').get_text(strip=True)

        database = sqlite3.connect('gazetauz.db')
        cursor = database.cursor()
        cursor.execute('''
        INSERT OR IGNORE INTO categories(category_name, category_link) VALUES (?, ?)
        ''', (category_name, category_link))
        database.commit()
        cursor.execute('''
        SELECT category_id FROM categories
        WHERE category_name = ?
        ''', (category_name,))
        category_id = cursor.fetchone()[0]
        database.close()

        parser = CategoryParser(category_link, category_name, category_id)
        parser.get_data()


parsing()