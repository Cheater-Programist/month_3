from aiogram.dispatcher.filters.state import State, StatesGroup  # Memory
from aiogram.contrib.fsm_storage.memory import MemoryStorage  #Like a dispatcher's memory
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher import FSMContext  #
from config import anketa
import logging
import sqlite3

storage = MemoryStorage()

bot = Bot(token=anketa)
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

conn = sqlite3.connect('resume_bot.db')
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS resumes(
	id INTEGER PRIMARY KEY,
	full_name VARCHAR(255) NOT NULL,
	age INTEGER NOT NULL,
	email TEXT DEFAULT NULL,
	phone_number TEXT,
	experience INTEGER DEFAULT 0
)""")
conn.commit()


class ResumeState(StatesGroup):
	get_full_name = State()
	get_age = State()
	get_email = State()
	get_phone_number = State()
	get_experience = State()


@dp.message_handler(commands=['start', 'help'])  #[] - to use more commands in one
async def start(message:types.Message):
	await message.answer("Hello! To type an anket tap /resume")


@dp.message_handler(commands=['resume'])
async def start_resume(message:types.Message):
	await ResumeState.get_full_name.set()
	await message.answer("Type your full name")


@dp.message_handler(state=ResumeState.get_full_name)
async def full_name(message:types.Message, state:FSMContext):
	async with state.proxy() as data:
		data['full_name'] = message.text

	await ResumeState.next()
	await message.answer("Type your age")


@dp.message_handler(state=ResumeState.get_age)
async def age(message:types.Message, state:FSMContext):
	async with state.proxy() as data:
		data['age'] = message.text

	await ResumeState.next()
	await message.answer("Type your email")


@dp.message_handler(state=ResumeState.get_email)
async def email(message:types.Message, state:FSMContext):
	async with state.proxy() as data:
		data['email'] = message.text

	await ResumeState.next()
	await message.answer("Type your phone_number")


@dp.message_handler(state=ResumeState.get_phone_number)
async def phone_number(message:types.Message, state:FSMContext):
	async with state.proxy() as data:
		data['phone_number'] = message.text

	await ResumeState.next()
	await message.answer("Type your work experience")


@dp.message_handler(state=ResumeState.get_experience)
async def experience(message:types.Message, state:FSMContext):
	async with state.proxy() as data:
		data['experience'] = message.text

	cursor.execute("""INSERT OR REPLACE INTO resumes(id, full_name, age, email, phone_number, experience) 
		VALUES (?, ?, ?, ?, ?, ?)""", (message.from_user.id, data['full_name'], data['age'], data['email'], data['phone_number'], data['experience']))
	conn.commit()

	await state.finish()	
	await message.answer("We saved your info.")


executor.start_polling(dp)