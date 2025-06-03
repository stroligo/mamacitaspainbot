import os
import asyncio
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Comando /home
async def home_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏠 Bem-vindo ao MamacitaSpainBot!")

# URL para testar conexão
URL = "https://icp.administracionelectronica.gob.es/icpplus/index.html"

# Comando /test
async def test_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔎 Testando a conexão...")

    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(URL, headers=headers, timeout=5)
        status = response.status_code

        if status == 200:
            await update.message.reply_text("✅ Conexão aceita! Site acessível.")
        elif status in [401, 403]:
            await update.message.reply_text("⚠️ Internet não está na Espanha ou acesso bloqueado (status 401/403).")
        else:
            await update.message.reply_text(f"⚠️ Resposta inesperada do servidor: status {status}")
    except requests.exceptions.ConnectTimeout:
        await update.message.reply_text("❌ Timeout: não foi possível conectar (provável bloqueio geográfico).")
    except Exception as e:
        await update.message.reply_text(f"❌ Erro desconhecido: {e}")

async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("home", home_command))
    app.add_handler(CommandHandler("test", test_command))

    await app.run_polling()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError as e:
        # Para Replit que já possui um event loop rodando
        if "event loop is already running" in str(e):
            loop = asyncio.get_event_loop()
            loop.create_task(main())
            loop.run_forever()
        else:
            raise
