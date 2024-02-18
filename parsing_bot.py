from aiogram import Bot, Dispatcher, types, executor
from bs4 import BeautifulSoup
from config import parsing
import requests

bot = Bot(token=parsing)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.answer("Hello")

@dp.message_handler(commands='acer')
async def start(message:types.Message):
    await message.answer("Top labtops from Acer:")
    url = 'https://www.barmak.store/category/Acer/'
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, 'lxml')

    all_laptops_name = soup.find_all('div', class_ = "tp-product-tag-2")
    all_laptops_price = soup.find_all('span', class_ = "tp-product-price-2 new-price")
    
    for name, price in zip(all_laptops_name, all_laptops_price):
        await message.answer(f"Title: {name.text}Price: {price.text}")

@dp.message_handler(commands='asus')
async def start(message:types.Message):
    await message.answer("Top labtops from Asus:")
    url = 'https://www.barmak.store/category/Asus/'
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, 'lxml')

    all_laptops_name = soup.find_all('div', class_ = "tp-product-tag-2")
    all_laptops_price = soup.find_all('span', class_ = "tp-product-price-2 new-price")
    all_laptops_image = soup.find_all('img', class_ = "image-size-cls")

    
    for name, price in zip(all_laptops_name, all_laptops_price):
        await message.answer(f"Title: {name.text}Price: {price.text}")
 
executor.start_polling(dp)