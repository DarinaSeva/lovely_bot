import logging
import os
import re
import requests
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters.command import Command 


GIPHY_API_KEY = 'N8MJuWNWONQ1mqhSpAEsyu2tkC8Jz2qC'

TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO, filename="mylog.txt", 
                    format='%(asctime)s, %(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S')

def get_funny_gif():
    url = f'https://api.giphy.com/v1/gifs/random?api_key={GIPHY_API_KEY}&tag=funny'
    response = requests.get(url)
    data = response.json()
    gif_url = data['data']['images']['original']['url']
    return gif_url

async def send_funny_gif(message: Message):
    gif_url = get_funny_gif()
    await message.answer_animation(animation=gif_url)

def contains_cyrillic(text):
    return bool(re.search('[а-яА-Я]', text))

translit_dict = {
    'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'E', 'Ж': 'Zh',
    'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O',
    'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'H', 'Ц': 'Ts',
    'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Shch', 'Ъ': '', 'Ы': 'Y', 'Ь': '', 'Э': 'E', 'Ю': 'Yu',
    'Я': 'Ya', 'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
    'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
    'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h',
    'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e',
    'ю': 'yu', 'я': 'ya', ' ': ' ', '-': '-'
}

def transliterate(text):
    return ''.join([translit_dict.get(char, char) for char in text])

@dp.message(Command(commands=['start']))
async def process_command_start(message: Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    if contains_cyrillic(user_name):
        transliterated_name = transliterate(user_name)
    else:
        transliterated_name = user_name  
    text = f'Приветики, {transliterated_name}!'
    logging.info(f'{user_name}, {user_id} запустил самый лучший бот на свете')
    await bot.send_message(chat_id=user_id, text=text)

@dp.message(Command(commands=['funnygif']))
async def command_funny_gif(message: Message):
    await send_funny_gif(message)

@dp.message()
async def echo_message(message: Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    text = message.text
    logging.info(f'{user_name}, {user_id}, {text}')
    await message.answer(text=text)

if __name__ == '__main__':
    dp.run_polling(bot)