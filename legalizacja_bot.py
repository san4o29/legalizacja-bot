import os
import openai
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("Telegram_bot")
openai.api_key = os.getenv("")

LANGUAGES = ['🇺🇦 Українська', '🇬🇧 English', '🇷🇺 Русский', '🇪🇸 Español', '🇮🇩 Bahasa Indonesia']

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton(lang)] for lang in LANGUAGES]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Привіт! Обери мову:", reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Ти експерт з легалізації в Польщі. Відповідай чітко, коротко, корисно."},
            {"role": "user", "content": user_text}
        ]
    )
    await update.message.reply_text(response.choices[0].message.content)

app = Application.builder().token(os.getenv("BOT_TOKEN")).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == "__main__":
    app.run_polling()
