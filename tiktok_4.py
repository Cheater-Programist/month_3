from config import tiktok
import requests, os, logging
from tik_tok_downloader_4 import installing
from aiogram import Bot, Dispatcher, types, executor


bot = Bot(tiktok)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.reply(f"Hello {message.from_user.full_name}, send a tiktok link...")

@dp.message_handler()
async def get_url_tiktok(message:types.Message):
    if 'tiktok.com' in message.text:
        await message.reply("Start installing video...")
        installing(message.text)
        a = message.text.split('/')[5].split('?')[0]
        with open(f'video/{a}.mp4', 'rb') as my_video:
            await message.answer_video(my_video)
    else:
        await message.reply("I didn't got it, please send a tiktok link!")

executor.start_polling(dp)