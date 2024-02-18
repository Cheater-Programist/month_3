from aiogram import Bot, Dispatcher, types, executor
from config import token
import random, logging, aiohttp
from aiohttp import ClientSession

bot = Bot(token=token)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

start_inline_buttons = [
    types.InlineKeyboardButton('Получить локацию', callback_data='get_location'),
    types.InlineKeyboardButton('Наш сайт', url='https://geeks.kg/')
]
start_inline_keyboard = types.InlineKeyboardMarkup().add(*start_inline_buttons)

@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer(f"Привет {message.from_user.full_name}", reply_markup=start_inline_keyboard)

async def is_land(latitude, longitude):
    async with ClientSession() as session:
        async with session.get(f"https://nominatim.openstreetmap.org/reverse?lat={latitude}&lon={longitude}&format=json") as response:
            if response.status == 200:
                data = await response.json()
                # Проверяем, есть ли информация о местности
                return 'osm_type' in data and data['osm_type'].lower() != 'water'
            return False

@dp.callback_query_handler(lambda call: call.data == "get_location")
async def get_random_location(callback: types.CallbackQuery):
    await callback.message.answer("Высылаю случайные координаты")
    while True:
        latitude = random.uniform(-90.000000, 90.000000)
        longitude = random.uniform(-180.000000, 180.000000)
        if await is_land(latitude, longitude):
            await callback.message.answer(f'{latitude} {longitude}')
            await callback.message.answer_location(latitude=latitude, longitude=longitude, reply_markup=start_inline_keyboard)
            break

executor.start_polling(dp)
