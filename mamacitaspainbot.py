# mamacitaspainbot.py
import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

load_dotenv()

TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
URL_CITA = "https://icp.administracionelectronica.gob.es/icpplus/acEntrada"
URL_TEST = "https://icp.administracionelectronica.gob.es/icpplus/index.html"

def check_disponibilidade():
    try:
        session = requests.Session()
        headers = {"User-Agent": "Mozilla/5.0"}
        response = session.get(URL_CITA, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        select = soup.find("select", {"name": "provincias"})
        if not select:
            return False
        provincias = [opt.text.strip() for opt in select.find_all("option")]
        return any("valencia" in p.lower() for p in provincias)
    except Exception as e:
        print("Erro:", e)
        return False

async def home_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔎 Iniciando verificação de disponibilidade para VALENCIA...")

    async def monitor():
        while True:
            if check_disponibilidade():
                await update.message.reply_text("🚨 Pode haver disponibilidade de cita para VALENCIA. Verifique no site oficial.")
                break
            else:
                print("Nada disponível. Verificando novamente em 10 minutos.")
            await asyncio.sleep(600)

    import asyncio
    asyncio.create_task(monitor())

async def test_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🌐 Testando conexão com o site do governo espanhol...")
    try:
        response = requests.get(URL_TEST, timeout=10)
        if response.status_code == 200:
            await update.message.reply_text("✅ Conexão aceita! Parece que você está acessando da Espanha ou via proxy.")
        else:
            await update.message.reply_text(f"⚠️ Resposta inesperada. Código: {response.status_code}")
    except requests.exceptions.RequestException:
        await update.message.reply_text("❌ Não foi possível acessar o site. Provavelmente você está fora da Espanha.")
