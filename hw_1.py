from aiogram import Bot, Dispatcher, types, executor
import random
from config import hw_1

bot = Bot(token=hw_1)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.answer(' Я загадал число от 1 до 3 угадайте')

a = random.randint(1, 3)

@dp.message_handler(text = ['1'])
async def start(message:types.Message):
    if 1 == a:
        await message.answer_photo('https://media.makeameme.org/created/you-win-nothing-b744e1771f.jpg')
    else:
        await message.answer_photo('https://media.makeameme.org/created/sorry-you-lose.jpg')

@dp.message_handler(text = ['2'])
async def start(message:types.Message):
    if 2 == a:
        await message.answer_photo('https://media.makeameme.org/created/you-win-nothing-b744e1771f.jpg')
    else:
        await message.answer_photo('https://media.makeameme.org/created/sorry-you-lose.jpg')

@dp.message_handler(text = ['3'])
async def start(message:types.Message):
    if 3 == a:
        await message.answer_photo('https://media.makeameme.org/created/you-win-nothing-b744e1771f.jpg')
    else:
        await message.answer_photo('https://media.makeameme.org/created/sorry-you-lose.jpg')

executor.start_polling(dp)