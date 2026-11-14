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
    return "Bot Disionariu Tetum-Baikenu ativu hela!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host="0.0.0.0", port=port)
# ----------------------------------------

# DATABASE KAMUS LOKAL (Tetum -> Dawan)
# Anda bisa terus menambah daftar kata di sini nanti
KAMUS_TETUM_DAWAN = {
    "bee": {
        "dawan": "Oel",
        "kelas": "Noun (Kata Benda)",
        "contoh": "Bee manas (Oe maputu)"
    },
    "haan": {
        "dawan": "Tah",
        "kelas": "Verb (Kata Kerja)",
        "contoh": "Mai ita haan (Oum he tah)"
    },
    "bainhira": {
        "dawan": "Leka",
        "kelas": "Adverb",
        "contoh": "Bainhira ita bá (Leka ni tnao)"
    },
    "ema": {
        "dawan": "Atoin",
        "kelas": "Noun",
        "contoh": "Ema Oecusse (Atoin Meto)"
    },
    "di'ak": {
        "dawan": "Naleok",
        "kelas": "Adjective / Verb",
        "contoh": "Nia di'ak loos (In naleok neuba)"
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Ola! 🤖 Bot Disionariu **Tetum ➔ Baikenu (Uab Meto)**.\n\n"
        "Favor hakerek liafuan **Tetum**, no bot sei traduz ba Baikenu."
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
    
    print("Bot Disionariu Tetum-Baikenu lao hela...")
    application.run_polling()
