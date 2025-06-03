# main.py
import asyncio
import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler

from mamacitaspainbot import home_handler
from test_conection import test_command

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("home", home_handler))
    app.add_handler(CommandHandler("test", test_command))

    print("🤖 Bot rodando... Comandos: /home, /test")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
