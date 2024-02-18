from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.storage import FSMContext
import logging, sqlite3, time
from config import bank

# ========================================================================================================================================

"""
Начинаем писать бот
"""

bot = Bot(token=bank)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

# ========================================================================================================================================

"""
Создаем базу данных Пользователи 
"""

user_connection = sqlite3.connect('users.db')
user_cursor = user_connection.cursor()

# ========================================================================================================================================

"""
Создаем базу данных Переводы
"""

transfer_connection = sqlite3.connect('transfers.db')
transfer_cursor = transfer_connection.cursor()

# ========================================================================================================================================

"""
Какие данные должена иметь база данных пользователь
"""

user_cursor.execute("""CREATE TABLE IF NOT EXISTS user(
    id VARCHAR(255),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    passport_id VARCHAR(255),
    created VARCHAR(255),
    balance INTEGER DEFAULT 0
);
""")
user_connection.commit()

# ========================================================================================================================================

"""
Сеэйты для регистрации
"""

class RegistrationState(StatesGroup):
    first_name = State()
    last_name = State()
    passport_id = State()
    balance = State()
    
# ========================================================================================================================================

"""
Какие данные нужны для базы данных Перевод
"""

transfer_cursor.execute('''CREATE TABLE IF NOT EXISTS transfer(
    id INTEGER PRIMARY KEY,
    sender_id VARCHAR(255),
    taker_id VARCHAR(255),
    amount INTEGER,
    created VARCHAR(255)
)''')
transfer_connection.commit()

# ========================================================================================================================================

"""
Стэйты для базы данных Перевод
"""

class TransferingState(StatesGroup):
    sender_id = State()
    taker_id = State()
    amount = State()

# ========================================================================================================================================

"""
Комманда старт, сначала мы проверям зарегистрирован пользователь или нет, если нет, то бот приветствует, и начинаеться регистрация, а если да, то он выдает мини информацию о боте.
"""

@dp.message_handler(commands='start')
async def start(message:types.Message, state:FSMContext):
    user_cursor.execute(f"SELECT id FROM user WHERE id = {message.from_user.id};")   
    user_connection.commit()
    result = user_cursor.fetchall()
    if result == []:
        async with state.proxy() as data:
            data['id'] = message.from_user.id
        await message.answer("Hello, please sign up:")
        a = time.sleep(0.7)
        await message.answer("Your name?")
        await RegistrationState.first_name.set()

# ========================================================================================================================================

        @dp.message_handler(state=RegistrationState.first_name)
        async def get_last_name(message:types.Message, state:FSMContext):
            async with state.proxy() as data:
                data['first_name'] = message.text
            await message.answer("Your surname?")
            await RegistrationState.next()

# ========================================================================================================================================

        @dp.message_handler(state=RegistrationState.last_name)
        async def get_phone(message:types.Message, state:FSMContext):
            async with state.proxy() as data:
                data['last_name'] = message.text
            await message.answer("Your passport id?")
            await RegistrationState.next()

# ========================================================================================================================================

        @dp.message_handler(state=RegistrationState.passport_id)
        async def get_passport_id(message:types.Message, state:FSMContext):
            async with state.proxy() as data:
                data['passport_id'] = message.text
                data['created'] = time.ctime()
            await RegistrationState.last()
            await message.answer("Congratulations! You signed up successfuly")
            b = time.sleep(0.6)
            user_cursor.execute(f"INSERT INTO user(id, first_name, last_name, passport_id, created) VALUES (?, ?, ?, ?, ?)", (data['id'], data['first_name'], data['last_name'], data['passport_id'], data['created']))
            user_connection.commit()
            await message.answer(f"""Здраствуйте {data['first_name']} {data['last_name']}!\nС помощью нашего банка вы можете узнать свой баланс нажав: /balance\nи так же, делать переводы нажав: /transfer\nP.S. Переобнавляйте ботаб после каждой процедуры""")
        
# ========================================================================================================================================

    else:
        user_cursor.execute(f"SELECT first_name, last_name FROM user WHERE id = {message.from_user.id};")
        user_connection.commit()
        result = user_cursor.fetchall()
        await message.answer(f"""Здраствуйте {result[0][0]}  {result[0][1]}!
С помощью нашего банка вы можете
узнать свой баланс нажав: /balance
и так же, делать переводы нажав: /transfer\nP.S. Переобнавляйте ботаб после каждой процедуры""")

# ========================================================================================================================================

"""
Команда баланс это команда проверяетб есть ли у пользователя счет или нет, если нет, то он спрашивает на сколько нужно пополнить и пополняет, а если есть, то просто показывает баланс пользователя.
"""

@dp.message_handler(commands='balance')
async def balance(message:types.Message, state:FSMContext):
    user_cursor.execute(f"SELECT balance FROM user WHERE id = {message.from_user.id};")
    user_connection.commit()
    result = user_cursor.fetchall()
    a = result[0][0]
    if result[0][0] == 0:
        await message.answer("You have to have a balance!")
        a = time.sleep(0.5)
        await message.answer("How much do you wanna top up?")
        await RegistrationState.balance.set()

# ========================================================================================================================================

        @dp.message_handler(state=RegistrationState.balance)
        async def get_balance(message:types.Message, state:FSMContext):
            async with state.proxy() as data:
                data['balance'] = int(message.text)
            await message.answer("Congratulations! You topped up your balance successfuly")
            print(f"{data['balance']} <=")
            print(f"{type(data['balance'])} <=")
            await RegistrationState.last()
            user_cursor.execute(f"UPDATE user SET balance = {data['balance']} WHERE id = {message.from_user.id}")
            user_connection.commit()

# ========================================================================================================================================

    else:
        user_cursor.execute(f"SELECT balance FROM user WHERE id = {message.from_user.id};")
        user_connection.commit()
        result = user_cursor.fetchall()
        # async with state.proxy() as data:
        await message.answer(f"Your balance: {a}")

# ========================================================================================================================================

"""
Команда переводы, она запрашивает у пользователя сумму которую он хочет перевести, если сумма превышает его баланс, то бот ему выводит, Не достаточно средств, если не превышает, то бот запрашивает id пользователя которому пользователь хочет отправить деньги, и если он находит получателя, то отправлят деньги и уведомляет обеих, а если нет, то выводит то что нет пользователя с таким id.
"""

@dp.message_handler(commands='transfer')
async def transfer(message:types.Message, state:FSMContext):
    await message.answer("How much do you want to transfer?")
    await TransferingState.amount.set()

# ========================================================================================================================================

@dp.message_handler(state=TransferingState.amount)
async def get_balance(message:types.Message, state:FSMContext):
    blnc = 0
    user_cursor.execute(f"SELECT balance FROM user WHERE id = {message.from_user.id};")
    user_connection.commit()
    result = user_cursor.fetchall()
    if int(message.text) > result[0][0]:
        await message.answer("You don't have anough money.")

    else:
        async with state.proxy() as data:
            data['sender_id'] = message.from_user.id
            data['amount'] = int(message.text)
            blnc = data['amount']
        await message.answer("Who do you wanna transfer? (ID)")
        await TransferingState.taker_id.set()

# ========================================================================================================================================
        
        @dp.message_handler(state=TransferingState.taker_id)
        async def id(message:types.Message, state:FSMContext):
            user_cursor.execute(f"SELECT id FROM user WHERE id = {message.text}")
            user_connection.commit()
            result = user_cursor.fetchall()
            await TransferingState.last()
            if result == []:
                await message.answer(f"Not found user with this {message.text} id")
            else:
                async with state.proxy() as data:
                    data['taker_id'] = message.text
                    data['created'] = time.asctime()
                await bot.send_message(data['taker_id'], f"Your balance topped up for {data['amount']}$")
                await message.answer("Your transfer transfered successfuly")
                user_cursor.execute("""BEGIN""")
                transfer_cursor.execute(f"INSERT INTO transfer(sender_id, taker_id, amount, created) VALUES (?, ?, ?, ?)", (data['sender_id'], data['taker_id'], data['amount'], data['created']))
                transfer_connection.commit()
                user_cursor.execute(f"UPDATE user SET balance = balance + {data['amount']} WHERE id = {message.text}")
                user_cursor.execute(f"UPDATE user SET balance = balance - {data['amount']} WHERE id = {message.from_user.id}")
                user_connection.commit()
                user_cursor.execute("""COMMIT""")

# ========================================================================================================================================

executor.start_polling(dp)