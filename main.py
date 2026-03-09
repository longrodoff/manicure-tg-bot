import asyncio
import csv
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

load_dotenv()
API_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="💅 Прайс-лист"),
            KeyboardButton(text="🗓 Записаться на ноготочки")
        ],
        [
            KeyboardButton(text="📍 Как нас найти?")
        ]
    ],
    resize_keyboard=True
)

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    with open("clients.csv", "a", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([user_id, user_name, "Нажал /start"])

    await message.answer(
        f"Здравствуйте, {user_name}! 🌸 Добро пожаловать в нашу студию маникюра. Выберите нужный раздел в меню ниже:",
        reply_markup=main_kb
    )

@dp.message(F.text == "💅 Прайс-лист")
async def price_handler(message: types.Message):
    await message.answer(
        "✨ Наш прайс-лист:\n\n"
        "• Маникюр без покрытия — 1000 ₽\n"
        "• Маникюр + гель-лак — 1800 ₽\n"
        "• Наращивание ногтей — 2500 ₽\n"
        "• Френч/Дизайн — от 300 ₽\n\n"
        "Все инструменты проходят 3 этапа стерилизации! 💯"
    )

@dp.message(F.text == "🗓 Записаться на ноготочки")
async def book_handler(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    with open("clients.csv", "a", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([user_id, user_name, "Перешел к записи"])

    book_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✍️ Написать администратору", url="https://t.me/durov")
            ]
        ]
    )

    await message.answer(
        "Отлично! Чтобы подобрать удобное окошко, напишите нашему администратору. Она на связи и быстро ответит 👇",
        reply_markup=book_kb
    )

@dp.message(F.text == "📍 Как нас найти?")
async def location_handler(message: types.Message):
    await message.answer("Мы находимся по адресу: г. Москва, ул. Красивая, д. 1 (5 минут от метро). Ждем вас в гости! ☕️🍬")

@dp.message()
async def echo_handler(message: types.Message):
    await message.answer("Пожалуйста, воспользуйтесь кнопочками меню внизу экрана 👇", reply_markup=main_kb)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())