from aiogram import Bot, Dispatcher, types, executor

bot = Bot(token='6843613788:AAGMP6KbFd2oh52snaAUD49fvHXr8Q-x2zA')
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start(massage:types.Message):
    await massage.answer("Hello World!, and Geeks")

@dp.message_handler(commands='help')
async def help(message:types.Message):
    await message.answer("How can I help you?")

@dp.message_handler(text='Geeks')
async def geeks(message:types.Message):
    await message.answer("Geeks")

@dp.message_handler(commands='test')
async def test(message:types.Message):
    print(message)
    # await message.answer(f"Hello {message.from_user.full_name}")
    # await message.answer(f'Your username is @{message.from_user.username}')
    # await message.reply("It's repling a text")
    # await message.answer_location(40.5193216724554, 72.8030109959693)
    # await message.answer_photo('https://data.kaktus.media/image/big/2023-07-21_18-00-13_831965.jpg')
    # await message.answer_contact('+996552878777', "Mukhammadamin", "Ibaydillayev")
    # await message.answer_dice(emoji="🎯")
    with open('voice.m4a', 'rb') as my_voice:
        await message.answer_voice(my_voice)
    with open('voice.m4a', 'rb') as my_voice:
        await message.answer_audio(my_voice)


@dp.message_handler()
async def not_found(message:types.Message):
    await message.reply("I didn't care, chose /help")


"""
@dp.message_handler()
async def get_number(message:types.Message):
    try:
        if isinstance(int(message.text), int):
            await message.answer("Это число")
    except:
        await message.answer("Это не число")
"""

executor.start_polling(dp)