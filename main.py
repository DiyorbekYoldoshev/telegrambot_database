from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler, Updater, Filters
import os
from inlines import inline_handler
from messages import message_handler
from send_buttons.send_menu import send_main_menu


def start(update, context):
    send_main_menu(context=context, chat_id=update.message.from_user.id)


def main():
    # token = os.getenv("TELEGRAM_BOT_TOKEN")
    updater = Updater(token="8006573821:AAEeC0iEQu2FCaohCOvRIh5Nc1-KSo4_4J0")
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, message_handler))
    dp.add_handler(CallbackQueryHandler(inline_handler))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
