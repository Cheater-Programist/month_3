from aiogram import Bot, Dispatcher, types, executor
from config import token
import logging

bot = Bot(token=token)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)


start_buttons = [
    types.KeyboardButton('About us'),
    types.KeyboardButton('Adress'),
    types.KeyboardButton('Courses'),
    types.KeyboardButton('Rolling in')
]
start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*start_buttons)  #if you wanna some, chose by index => .add(start_buttons[0]).add(start_buttons[1])

@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.answer(f"Hello {message.from_user.full_name}", reply_markup=start_keyboard)

@dp.message_handler(text="About us")
async def about_us(message:types.Message):
    await message.answer("Geels - it's IT courses in Bishkek, Osh, Kara-Balth and in Tashkent")

@dp.message_handler(text="Adress")
async def adress(message:types.Message):
    await message.answer("Our adress: Myrza Amatova 1B")
    await message.answer_location(40.5193216724554, 72.8030109959693)


courses_buttons = [
    types.KeyboardButton('BackEnd'),
    types.KeyboardButton('FrontEnd'),
    types.KeyboardButton('UX/UI'),
    types.KeyboardButton('Android'),
    types.KeyboardButton('IOS'),
    types.KeyboardButton('Back'),
]
courses_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*courses_buttons)

@dp.message_handler(text='Courses')
async def courses(message:types.Message):
    await message.answer("Here it's our courses: ", reply_markup=courses_keyboard)

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

@dp.message_handler()
async def not_found(message:types.Message):
    await message.reply("I didn't care, chose /start")


executor.start_polling(dp)