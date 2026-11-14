import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import requests

# Konfigura logging hodi kontrola aktividade bot
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Handler ba instrusaun /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Ola! 🤖 Hakerek liafuan Tetum nebe ita-bot hakarak buka nia signifikadu iha lian Baikenu (Uab Meto)."
    )

# Handler hodi prosesa mensajen (Liafuan nbe user manda)
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
    # Input Token BotFather iha ne
    TOKEN = "8928242028:AAGTIT6NmpicUr-D4mxxVSz4fquT_tUJORI"
    
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Rejista handler
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), search_dictionary))
    
    # Running bot
    print("Bot lao hela...")
    application.run_polling()