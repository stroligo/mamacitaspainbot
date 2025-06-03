import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TELEGRAM_TOKEN:
    raise ValueError("Erro: variável TELEGRAM_TOKEN não definida. Configure seu token no .env ou nas variáveis do Replit.")

async def home_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏠 Comando /home funcionando!")

async def test_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔎 Testando a conexão...")

    import requests

    URL = "https://icp.administracionelectronica.gob.es/icpplus/index.html"
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

    print("🤖 Bot rodando... Comandos: /home, /test")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
