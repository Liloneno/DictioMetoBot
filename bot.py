import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import requests
from flask import Flask
import threading
import os

# Konfigurasi logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# --- WEB SERVER SEDERHANA UNTUK RENDER ---
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "Bot Kamus Tetum-Dawan sedang aktif!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host="0.0.0.0", port=port)
# ----------------------------------------

# DATABASE KAMUS LOKAL (Tetum -> Dawan)
# Anda bisa terus menambah daftar kata di sini nanti
KAMUS_TETUM_DAWAN = {
    "bee": {
        "dawan": "Nono",
        "kelas": "Noun (Kata Benda)",
        "contoh": "Bee mamarin (Air bersih)"
    },
    "haan": {
        "dawan": "Kaen",
        "kelas": "Verb (Kata Kerja)",
        "contoh": "Hau hakarak haan tebes."
    },
    "bainhira": {
        "dawan": "Maupun / Tabes",
        "kelas": "Adverb",
        "contoh": "Bainhira ita bá..."
    },
    "ema": {
        "dawan": "Atoin",
        "kelas": "Noun",
        "contoh": "Ema Oecusse (Atoin Meto)"
    },
    "moris": {
        "dawan": "Mauri",
        "kelas": "Adjective / Verb",
        "contoh": "Moris di'ak."
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Ola! 🤖 Bot Kamus **Tetum ➔ Dawan (Uab Meto)**.\n\n"
        "Silakan ketik kata dalam bahasa **Tetum**, dan bot akan memberikan padanannya ke bahasa Dawan."
    )

async def translate_tetum_to_dawan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kata_input = update.message.text.strip().lower()
    
    # Cek apakah kata ada di database kamus kita
    if kata_input in KAMUS_TETUM_DAWAN:
        data = KAMUS_TETUM_DAWAN[kata_input]
        dawan_word = data["dawan"]
        kelas = data["kelas"]
        contoh = data["contoh"]
        
        reply_text = (
            f"📖 **Tetum:** `{kata_input.capitalize()}`\n"
            f"➔ **Dawan (Oecusse):** `*{dawan_word}*`\n\n"
            f"🏷 **Kelas Kata:** {kelas}\n"
            f"💡 **Contoh:** _{contoh}_"
        )
    else:
        reply_text = (
            f"❌ Deskulpa, liafuan **'{kata_input}'** seidauk iha ami-nia bazedadus (database).\n\n"
            f"Nau, ita bele hatutan liafuan foun iha tempu oin mai!"
        )

    await update.message.reply_text(reply_text, parse_mode='Markdown')

if __name__ == '__main__':
    # Jalankan server web di background thread untuk Render
    t = threading.Thread(target=run_web)
    t.start()

    TOKEN = os.getenv("TOKEN", "8928242028:AAGTIT6NmpicUr-D4mxxVSz4fquT_tUJORI")
    
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), translate_tetum_to_dawan))
    
    print("Bot Kamus Tetum-Dawan lao hela...")
    application.run_polling()
