import logging
import openai
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command

# Замените на свои токены
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

openai.api_key = OPENAI_API_KEY

@dp.message(Command("stop"))
async def stop_bot(message: Message):
    await message.answer("Бот выключается...")
    await bot.session.close()
    loop = asyncio.get_event_loop()
    loop.stop()

@dp.message()
async def chat_with_gpt(message: Message):
    user_text = message.text
    response = await get_gpt_response(user_text)
    await message.answer(response)

async def get_gpt_response(text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": text}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        logging.error(f"Ошибка при запросе к OpenAI: {e}")
        return "Ошибка при получении ответа. Попробуйте позже."

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
