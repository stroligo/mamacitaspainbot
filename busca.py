import asyncio
from telegram import Bot

TOKEN = "7602533921:AAGUYgqng7E1bI0lyorWHe70iwvuiwdOtKs"

async def main():
    bot = Bot(TOKEN)
    updates = await bot.get_updates()
    for u in updates:
        print("Chat ID:", u.message.chat.id)

asyncio.run(main())
