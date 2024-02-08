from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import ojak_kebab
from aiogram.dispatcher import FSMContext  
import logging
import sqlite3

storage = MemoryStorage()


bot = Bot(token=ojak_kebab)
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)
connect = sqlite3.connect('ojak_kebab_db.db')
cursor = connect.cursor()
connect2 = sqlite3.connect('ordering.db')
cursor2 = connect2.cursor()


cursor.execute('''CREATE TABLE IF NOT EXISTS ojak_kebab_db(
    id INTEGER PRIMARY KEY,
    username VARCHAR(255),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    date_joined VARCHAR(255)
    )''')
connect.commit()

cursor2.execute('''CREATE TABLE IF NOT EXISTS ordering(
    id INTEGER PRIMARY KEY,
    first_name VARCHAR(255),
    number VARCHAR(255),
    adress VARCHAR(255),
    food TEXT
    )''')
connect2.commit()

class OrderingState(StatesGroup):
    get_first_name = State()
    get_number = State()
    get_adress = State()
    get_food = State()


start_buttons = [
    types.KeyboardButton('Menu'),
    types.KeyboardButton('About us'),
    types.KeyboardButton('Adress'),
    types.KeyboardButton('To order')
]
start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*start_buttons)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    # print(message)
    await message.answer(f"Hello {message.from_user.full_name}", reply_markup=start_keyboard)
    cursor.execute(f'''INSERT INTO ojak_kebab_db(username, first_name, last_name, date_joined) VALUES('{message.from_user.username}', '{message.from_user.first_name}', '{message.from_user.last_name}', '{message.date}')''')
    connect.commit()

@dp.message_handler(text='Menu')
async def menu(message:types.Message):
    await message.answer_photo('https://nambafood.kg/dish_image/163137.png')
    await message.answer("Форель на мангале целиком")
    await message.answer_photo('https://nambafood.kg/dish_image/163145.png')
    await message.answer("Форель на мангале кусочками")
    await message.answer_photo('https://nambafood.kg/dish_image/48353.png')
    await message.answer("Шашлык из курицы")
    await message.answer_photo('https://nambafood.kg/dish_image/150933.png')
    await message.answer("Шашлык из баранины")
    await message.answer_photo('https://nambafood.kg/dish_image/163141.png')
    await message.answer("Сач кавурма с мясом")
    await message.answer_photo('https://nambafood.kg/dish_image/163144.png')
    await message.answer("Сач кавурма с курицей")
    await message.answer_photo('https://nambafood.kg/dish_image/173161.png')
    await message.answer("Вали кебап на 2 человека")
    await message.answer_photo('https://nambafood.kg/dish_image/150910.png')
    await message.answer("Вали кебаб на 4 человек")
    await message.answer_photo('https://nambafood.kg/dish_image/48339.png')
    await message.answer("Вали кебаб на 8 человек")
    await message.answer_photo('https://nambafood.kg/dish_image/173162.png')
    await message.answer("Маклюбе на 10-15человек")


@dp.message_handler(text='About us')
async def about_us(message:types.Message):
    await message.answer(f"""
        Ocak Kebap
Кафе "Ожак Кебап" на протяжении 18 лет радует своих гостей с изысканными турецкими блюдами в особенности своим кебабом.
Наше кафе отличается от многих кафе своими доступными ценами и быстрым сервисом.
В 2016 году по голосованию на сайте "Horeca" были удостоены "Лучшее кафе на каждый день" 
и мы стараемся оправдать доверие наших гостей.
Мы не добавляем консерванты, усилители вкуса, красители, ароматизаторы, растительные и животные жиры,
вредные добавки с маркировкой «Е». У нас строгий контроль качества: наши филиалы придерживаются норм Кырпотребнадзор и санэпидемстанции.
Мы используем только сертифицированную мясную и рыбную продукцию от крупных поставщиков.
    
Единый номер: +{996550799012}
""")
    
@dp.message_handler(text='Adress')
async def adress(message:types.Message):
    await message.answer_location(40.52654937013132, 72.79537129102678)
    await message.answer("234، 246 Курманжан-Датка ул., Ош")

# ordering_buttons = [
#     types.KeyboardButton('Форель на мангале целиком'),
#     types.KeyboardButton('Форель на мангале кусочками'),
#     types.KeyboardButton('Шашлык из курицы'),
#     types.KeyboardButton('Шашлык из баранины'),
#     types.KeyboardButton('Сач кавурма с мясом'),
#     types.KeyboardButton('Сач кавурма с курицей'),
#     types.KeyboardButton('Вали кебап на 2 человека'),
#     types.KeyboardButton('Вали кебаб на 4 человек'),
#     types.KeyboardButton('Вали кебаб на 8 человек'),
#     types.KeyboardButton('Маклюбе на 10-15человек')
# ]
# ordering_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*ordering_buttons)

@dp.message_handler(text='To order')
async def order_foor(message:types.Message):
    await OrderingState.get_first_name.set()
    await message.answer(f"What's your name?")


@dp.message_handler(state=OrderingState.get_first_name)
async def first_name(message:types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['first_name'] = message.text

    await OrderingState.next()
    await message.answer(f"What's your phone number?")


@dp.message_handler(state=OrderingState.get_number)
async def number(message:types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['number'] = message.text

    await OrderingState.next()
    await message.answer(f"What's your adress?")

@dp.message_handler(state=OrderingState.get_adress)
async def adress(message:types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['adress'] = message.text
    
    await OrderingState.next()
    await message.answer('What do you want?')
    await message.answer(f"Our menu: https://nambafood.kg/ojak-kebap")

@dp.message_handler(state=OrderingState.get_food)
async def food(message:types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['food'] = message.text


    cursor2.execute("""INSERT OR REPLACE INTO ordering(first_name, number, adress, food) VALUES (?, ?, ?, ?)""", (data['first_name'], data['number'], data['adress'], data['food']))
    connect2.commit()
    
    await state.finish()
    await message.answer('Thanks for ordering')
    await message.answer("Will be deliveried soon")


executor.start_polling(dp)