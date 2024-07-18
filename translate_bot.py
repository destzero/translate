from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from googletrans import Translator
import logging

TOKEN = '7252831938:AAEjm6uVMTulvfjVjJ5jEAHdzcgx3xs6O0U'

translator = Translator()

user_languages = {}

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_text(
        f'Salom, {user.first_name}! Qaysi tilni ishlatmoqchisiz? /uzbek, /english yoki /russian komandalaridan birini tanlang.'
    )

def set_uzbek(update: Update, context: CallbackContext) -> None:
    user_languages[update.effective_user.id] = 'uz'
    update.message.reply_text('Sizning tilingiz o\'zbek tiliga o\'zgartirildi.')

def set_english(update: Update, context: CallbackContext) -> None:
    user_languages[update.effective_user.id] = 'en'
    update.message.reply_text('Your language has been set to English.')

def set_russian(update: Update, context: CallbackContext) -> None:
    user_languages[update.effective_user.id] = 'ru'
    update.message.reply_text('Ваш язык был установлен на русский.')

def translate_text(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id in user_languages:
        dest_language = user_languages[user_id]
        translated = translator.translate(update.message.text, dest=dest_language)
        update.message.reply_text(translated.text)
    else:
        update.message.reply_text('Iltimos, avval tilni tanlang: /uzbek, /english yoki /russian.')

def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("uzbek", set_uzbek))
    dispatcher.add_handler(CommandHandler("english", set_english))
    dispatcher.add_handler(CommandHandler("russian", set_russian))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, translate_text))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
