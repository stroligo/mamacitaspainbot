import asyncio
import requests
from bs4 import BeautifulSoup
from telegram import Bot

TELEGRAM_TOKEN = "7602533921:AAGUYgqng7E1bI0lyorWHe70iwvuiwdOtKs"
TELEGRAM_CHAT_ID = "5010705669"
URL = "https://icp.administracionelectronica.gob.es/icpplus/acEntrada"

bot = Bot(token=TELEGRAM_TOKEN)

def check_disponibilidade():
    session = requests.Session()
    headers = {"User-Agent": "Mozilla/5.0"}
    response = session.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    select = soup.find("select", {"name": "provincias"})
    if not select:
        print("❌ Select 'provincias' não encontrado.")
        return False

    provincias = [opt.text.strip() for opt in select.find_all("option")]
    print("Provincias encontradas:", provincias)

    return any("valencia" in p.lower() for p in provincias)

async def send_alert(msg):
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)

async def main():
    await send_alert("🔎 Iniciando verificação de disponibilidade para VALENCIA...")
    while True:
        try:
            if check_disponibilidade():
                await send_alert("🚨 Pode haver disponibilidade de cita para VALENCIA. Verifique no site oficial.")
                print("Mensagem enviada. Finalizando o script.")
                break
            else:
                print("Nada disponível. Verificando novamente em 10 minutos.")
        except Exception as e:
            print("Erro:", e)

        await asyncio.sleep(600)

if __name__ == "__main__":
    asyncio.run(main())
