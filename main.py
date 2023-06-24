import os
import time

from dotenv import load_dotenv
import sqlite3
from aiogram import Dispatcher, Bot, executor
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from keyboards import generate_buttons
from database import create_database
from parser import parsing

database = sqlite3.connect('gazetauz.db')
cursor = database.cursor()

load_dotenv()
token = os.getenv('TOKEN')

storage = MemoryStorage()
bot = Bot(token=token)
dp = Dispatcher(bot, storage=storage)


class Questions(StatesGroup):
    category = State()
    one_category = State()
    lot_category = State()


@dp.message_handler(commands=['start', 'about', 'help', '5', '10', '20'])
async def default_commands(message: Message):
    if message.text == '/start':
        await message.answer('Добро пожаловать в новостной бот!\nНажмите \'/\' и выберите нужную Вам функцию')
    elif message.text == '/about':
        await message.answer(
            'Этот бот был создан для того, чтобы информировать вас о том, что происходит в Узбекистане.')
    elif message.text == '/help':
        await message.answer('Если у вас возникли проблемы или предложения, пишите сюда: @bobrarity')

    elif message.text == '/5':
        await Questions.category.set()
        await message.answer('Выберите категорию: ', reply_markup=generate_buttons())
    elif message.text == '/10':
        await Questions.one_category.set()
        await message.answer('Выберите категорию: ', reply_markup=generate_buttons())
    elif message.text == '/20':
        await Questions.lot_category.set()
        await message.answer('Выберите категорию: ', reply_markup=generate_buttons())


@dp.message_handler(content_types=['text'], state=Questions.category)
async def latest_five(message: Message, state: FSMContext):
    if message.text in ['/start', '/about', '/help']:
        await state.finish()
        await default_commands(message)
    else:
        cursor.execute(f'''
        SELECT category_name, info_name, info_time, info_desc, info_link FROM info
        JOIN categories ON categories.category_id = info.category_id
        WHERE category_name = '{message.text}'
        LIMIT 5;
        ''')
        news = cursor.fetchall()
        for one in news:
            await message.answer(
                f'Выбранная категория: {one[0]}\n\n{one[1]}\n\n{one[3]}\n\n{one[2]}\n\nСсылка: {one[4]}',
                reply_markup=ReplyKeyboardRemove())
            await state.finish()


@dp.message_handler(content_types=['text'], state=Questions.one_category)
async def latest_ten(message: Message, state: FSMContext):
    if message.text in ['/start', '/about', '/help']:
        await state.finish()
        await default_commands(message)
    else:
        cursor.execute(f'''
        SELECT category_name, info_name, info_time, info_desc, info_link FROM info
        JOIN categories ON categories.category_id = info.category_id
        WHERE category_name = '{message.text}'
        LIMIT 10;
        ''')
        news = cursor.fetchall()
        for one in news:
            await message.answer(
                f'Выбранная категория: {one[0]}\n\n{one[1]}\n\n{one[3]}\n\n{one[2]}\n\nСсылка: {one[4]}',
                reply_markup=ReplyKeyboardRemove())
            await state.finish()


@dp.message_handler(content_types=['text'], state=Questions.lot_category)
async def latest_twenty(message: Message, state: FSMContext):
    if message.text in ['/start', '/about', '/help']:
        await state.finish()
        await default_commands(message)
    else:
        cursor.execute(f'''
        SELECT category_name, info_name, info_time, info_desc, info_link FROM info
        JOIN categories ON categories.category_id = info.category_id
        WHERE category_name = '{message.text}'
        LIMIT 20;
        ''')
        news = cursor.fetchall()
        for one in news:
            await message.answer(
                f'Выбранная категория: {one[0]}\n\n{one[1]}\n\n{one[3]}\n\n{one[2]}\n\nСсылка: {one[4]}',
                reply_markup=ReplyKeyboardRemove())
            await state.finish()


executor.start_polling(dp)


def update_database():
    create_database()
    parsing()


while True:
    update_database()
    time.sleep(1800)
