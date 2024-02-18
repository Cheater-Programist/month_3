from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.storage import FSMContext
import logging, sqlite3, time
from config import token

# ========================================================================================================================================

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

# ========================================================================================================================================

connection = sqlite3.connect('itbot.db')
cursor = connection.cursor()

connection2 = sqlite3.connect('applications.db')
cursor2 = connection2.cursor()

# ========================================================================================================================================

cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    id VARCHAR(255),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    username VARCHAR(255),
    created VARCHAR(255)
);
""")
connection.commit()

cursor2.execute("""CREATE TABLE IF NOT EXISTS application(
    id INTEGER PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    phone VARCHAR(255),
    direction VARCHAR(255),
    note TEXT,
    created VARCHAR(255)
);
""")
connection2.commit()

# ========================================================================================================================================

start_buttons = [
    types.KeyboardButton('About us'),
    types.KeyboardButton('Adress'),
    types.KeyboardButton('Courses'),
    types.KeyboardButton('To applicate')
]
start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*start_buttons)  #if you wanna some, chose by index => .add(start_buttons[0]).add(start_buttons[1])

# ========================================================================================================================================

@dp.message_handler(commands='start')
async def start(message:types.Message):
    cursor.execute(f"SELECT id FROM users WHERE id = {message.from_user.id};")
    result = cursor.fetchall()  #saves, enters what has called before
    if result == []:
        cursor.execute(f'INSERT INTO users VALUES (?, ?, ?, ?, ?)', (message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username, time.ctime()))
        cursor.connection.commit()
    await message.answer(f"Hello {message.from_user.full_name}", reply_markup=start_keyboard)

# ========================================================================================================================================

@dp.message_handler(text="About us")
async def about_us(message:types.Message):
    await message.answer("Geels - it's IT courses in Bishkek, Osh, Kara-Balth and in Tashkent")

# ========================================================================================================================================

@dp.message_handler(text="Adress")
async def adress(message:types.Message):
    await message.answer("Our adress: Myrza Amatova 1B")
    await message.answer_location(40.5193216724554, 72.8030109959693)

# ========================================================================================================================================

courses_buttons = [
    types.KeyboardButton('BackEnd'),
    types.KeyboardButton('FrontEnd'),
    types.KeyboardButton('UX/UI'),
    types.KeyboardButton('Android'),
    types.KeyboardButton('IOS'),
    types.KeyboardButton('Back'),
]
courses_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*courses_buttons)

# ========================================================================================================================================

@dp.message_handler(text='Courses')
async def courses(message:types.Message):
    await message.answer("Here it's our courses: ", reply_markup=courses_keyboard)

# ========================================================================================================================================

@dp.message_handler(text='BackEnd')
async def backend(message:types.Message):
    await message.reply("BackEnd - it's back side of site that you never see")

@dp.message_handler(text='FrontEnd')
async def frontend(message:types.Message):
    await message.reply("FrontEnd - it's front side of site that you always see")

@dp.message_handler(text='UX/UI')
async def ux_ui(message:types.Message):
    await message.reply("UX/UI - it's design of site or app")

@dp.message_handler(text='Android')
async def android(message:types.Message):
    await message.reply("Android - it's an app for OS Android")

@dp.message_handler(text='IOS')
async def ios(message:types.Message):
    await message.reply("IOS - it's an app for OS Apple")

@dp.message_handler(text='Back')
async def rollback(message:types.Message):
    await start(message)

# ========================================================================================================================================

class ApplicationState(StatesGroup):
    first_name = State()
    last_name = State()
    phone = State()
    direction = State()
    note = State()

# ========================================================================================================================================

note_buttons = [
    types.KeyboardButton('Yes'),
    types.KeyboardButton('No'),
]
notes_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*note_buttons)

# ========================================================================================================================================

@dp.message_handler(text="To applicate")
async def to_applicate(message:types.Message):
    await message.answer("To get lids, you have to type next info:")
    await message.answer("Name, Surname, Number, direction, note(if have)")
    await message.answer("Your name?")
    await ApplicationState.first_name.set()

# ========================================================================================================================================

@dp.message_handler(state=ApplicationState.first_name)
async def get_last_name(message:types.Message, state:FSMContext):
    await state.update_data(first_name=message.text)
    await message.answer("Your surnmae?")
    await ApplicationState.next()

@dp.message_handler(state=ApplicationState.last_name)
async def get_phone(message:types.Message, state:FSMContext):
    await state.update_data(last_name=message.text)
    await message.answer("Your phone number?")
    await ApplicationState.next()

@dp.message_handler(state=ApplicationState.phone)
async def get_direction(message:types.Message, state:FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("Your direction?", reply_markup=courses_keyboard)
    await ApplicationState.next()

@dp.message_handler(state=ApplicationState.direction)
async def get_note(message:types.Message, state:FSMContext):
    await state.update_data(direction=message.text)
    await message.answer("Do you have note?")  # reply_markup=notes_keyboard)
    await ApplicationState.next()

@dp.message_handler(state=ApplicationState.note)
async def get_note(message:types.Message, state:FSMContext):
    await state.update_data(note=message.text)
    await ApplicationState.last()
    await message.answer("Information saved")
    result = await storage.get_data(user=message.from_user.id)
    # res = await state.get_data()
    send_message = f"""Заявка на курсы {time.ctime()}
Имя: {result['first_name']}
Фамилия: {result['last_name']}
Номер: {result['phone']}
Направление: {result['direction']}
Примечание: {result['note']}
Дата: {time.ctime()}"""
    cursor2.execute(f'INSERT INTO application(first_name, last_name, phone, direction, note, created) VALUES (?, ?, ?, ?, ?, ?)', (result['first_name'], result['last_name'], result['phone'], result['direction'], result['note'], time.ctime()))
    connection2.commit()
    await message.answer(f"{send_message}")
    await bot.send_message(-4142647964, f'{send_message}')
    
    
# ========================================================================================================================================

@dp.message_handler()
async def not_found(message:types.Message):
    await message.reply("I didn't care, chose /start")

# ========================================================================================================================================

executor.start_polling(dp)