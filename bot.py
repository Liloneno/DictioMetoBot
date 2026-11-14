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
    return "Bot Telegram Kamus sedang aktif!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host="0.0.0.0", port=port)
# ----------------------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Ola! 🤖 Hakerek liafuan Tetum nebe ita-bot hakarak buka nia signifikadu iha lian Baikenu (Uab Meto)."
    )

async def search_dictionary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    word = update.message.text.strip().lower()
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()[0]
            word_title = data.get('word', word).capitalize()
            meanings = data['meanings'][0]
            part_of_speech = meanings.get('partOfSpeech', 'N/A')
            definition = meanings['definitions'][0].get('definition', 'Laiha definisaun.')
            
            reply_text = f"📖 **{word_title}** *({part_of_speech})*\n\n🔹 **Signifikadu:** {definition}"
        else:
            reply_text = f"❌ Deskulpa, liafuan **'{word}'** seidauk eziste."
    except Exception as e:
        reply_text = "Akontese error wainhira konekta ba server disionariu."

    await update.message.reply_text(reply_text, parse_mode='Markdown')

if __name__ == '__main__':
    # Jalankan server web di background thread agar port Render tidak timeout
    t = threading.Thread(target=run_web)
    t.start()

    TOKEN = "8928242028:AAGTIT6NmpicUr-D4mxxVSz4fquT_tUJORI"
    
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), search_dictionary))
    
    print("Bot lao hela...")
    application.run_polling()
