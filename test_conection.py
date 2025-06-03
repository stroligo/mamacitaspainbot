import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

URL = "https://icp.administracionelectronica.gob.es/icpplus/index.html"

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

# Configuração do bot e adicionando o handler
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    load_dotenv()
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("test", test_command))
    application.run_polling()
