import os
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater, ConversationHandler
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

from telegram import KeyboardButton, ReplyKeyboardMarkup, BotCommand, ChatAction, Update
import sqlite3
from hisob import start, info, hisob, balans, sql_query, foydalanuvchilarni_korish
from hisob import (
    hisobni_toldirish,
    main_menu,
    start_toldirish,
    pul_otqazish,
    KIMGA_OTQAZISH,
    MIQDOR_KIRITISH,
    kimga_otqazish,
    miqdor_kiritish,
    tolovlar_tarixi,
    get_cancel_keyboard,
)
import re
load_dotenv()

database_path = "tr_bot.db"
ADMIN_ID = 1954153232
import logging


# Logging konfiguratsiyasi
logging.basicConfig(
    level=logging.INFO,  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()          #
    ]
)



def cancel(update, context):
    update.message.reply_text(text="❌ Bot to‘xtatildi.")
    return ConversationHandler.END


def register(update, context):
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    reply_text = "📱 Telefon raqamingizni ulashing"
    reply_markup = ReplyKeyboardMarkup([
        [KeyboardButton(text="📞 Kontaktni ulashish", request_contact=True)]
    ], resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text(text=reply_text, reply_markup=reply_markup)
    return "Phone_number"


def phone_number(update, context):
    contact = update.message.contact
    if contact and getattr(contact, "phone_number", None):
        phone = contact.phone_number
    else:
        text = update.message.text.strip()
        # oddiy validatsiya (+998901234567 yoki 9-15 raqam)
        if not re.match(r'^\+?\d{9,15}$', text):
            update.message.reply_text("Iltimos telefon raqamini +998... formatida yuboring yoki 'Kontaktni ulashish' tugmasini bosing.")
            return "Phone_number"
        phone = text

    context.user_data['phone_number'] = phone
    update.message.reply_text("✅ Qabul qilindi!\n\n✍️ Endi ismingizni kiriting:")
    return "Name"

def name(update, context):
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    name = update.message.text
    context.user_data['name'] = name
    update.message.reply_text(text="✅ Qabul qilindi!\n\n💳 Endi karta turi:")
    reply_markup = get_cancel_keyboard([
        [KeyboardButton(text="💳 HUMO"),KeyboardButton(text="💳 UZCARD")]
    ])
    update.message.reply_text(text="Quyidagilardn birini tanlang",reply_markup=reply_markup)


    return "Carta_type"

def card_type(update,context):
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    card_type = update.message.text
    context.user_data['card_type'] = card_type
    update.message.reply_text(text="Qabul qilindi! Carta raqam kiriting")
    return "Carta"

def carta(update, context):
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    try:
        text = update.message.text.strip()

        if len(text) != 16 or not text.isdigit():
            update.message.reply_text("⚠️ Karta raqami 16 ta raqamdan iborat bo‘lishi kerak!")
            return "Carta"

        user_id = update.effective_user.id
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE cart_number = ?", (text,))
        if cursor.fetchone():
            update.message.reply_text("⚠️ Bu karta boshqa foydalanuvchiga tegishli.")
            return "Carta"

        cursor.execute("SELECT cart_number FROM users WHERE id = ?", (user_id,))
        result = cursor.fetchone()
        if result and result[0] == text:
            update.message.reply_text("❌ Bu karta raqami avvaldan bor!")
            return "Carta"

        context.user_data['cart_number'] = text
        update.message.reply_text("✅ Karta raqami qabul qilindi!\n\n💰 Endi balansingizni kiriting:")
        return "Balance"
    except Exception as x:
        print(f"Xato bor: {x}")
        update.message.reply_text(text=f"⚠️ Xato: {x}")
        return "Carta"

from telegram.ext import ConversationHandler

def balance(update, context):
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    try:
        bal = update.message.text.strip()
        if not bal.isdigit():
            update.message.reply_text("⚠️ Balans faqat raqam bo‘lishi kerak!")
            return "Balance"

        bal = int(bal)
        if not (0 < bal < 100000000):
            update.message.reply_text("⚠️ Balans 0 va 100 000 000 oralig‘ida bo‘lishi kerak!")
            return "Balance"

        context.user_data['balance'] = bal

        # 🔹 Foydalanuvchini bazaga qo‘shish
        user = update.effective_user
        user_id = user.id
        username = f"@{user.username}" if user.username else "👤 Username yo'q"

        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (id, phone_number, name, card_type, cart_number, balance)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            context.user_data['phone_number'],
            context.user_data['name'],
            context.user_data['card_type'],
            context.user_data['cart_number'],
            context.user_data['balance'],
        ))
        conn.commit()
        conn.close()

        update.message.reply_text(
            f"🎉 <b>Ro‘yxatdan o‘tish muvaffaqiyatli!</b>\n\n"
            f"👤 <b>Ism:</b> {context.user_data['name']}\n"
            f"📛 <b>Username:</b> {username}\n"
            f"📱 <b>Telefon:</b> {context.user_data['phone_number']}\n"
            f"🎫 <b>Karta turi:</b> {context.user_data['card_type']}\n"
            f"💳 <b>Karta raqami:</b> {context.user_data['cart_number']}\n"
            f"💰 <b>Balans:</b> {context.user_data['balance']} so‘m\n",
            parse_mode="HTML",
        )

        reply_markup = ReplyKeyboardMarkup([
            ["🏠 Asosiy Menu", "📊 Balansni tekshirish", "To'liq malumot"],
            ["💰 Hisobni to'ldirish", "📜 To'lovlar tarixi", "💸 Pul o'tqazish"],
            ["❌ Cancel", "👥 Foydalanuvchilarni ko'rish"]
        ], resize_keyboard=True)

        update.message.reply_text("👇 Quyidagilardan birini tanlang:", reply_markup=reply_markup)

        context.bot.send_message(
            chat_id=ADMIN_ID,
            text=(f"📢 <b>Yangi foydalanuvchi qo‘shildi!</b>\n\n"
                  f"👤 <b>Ism:</b> {context.user_data['name']}\n"
                  f"📛 <b>Username:</b> {username}\n"
                  f"📱 <b>Telefon:</b> {context.user_data['phone_number']}\n"
                  f"🎫 <b>Karta turi:</b> {context.user_data['card_type']}\n"
                  f"💳 <b>Karta:</b> {context.user_data['cart_number']}\n"
                  f"💰 <b>Balans:</b> {context.user_data['balance']} so‘m"),
            parse_mode="HTML"
        )

        # ✅ Ro‘yxatdan o‘tish tugadi, ConversationHandler yopiladi
        return ConversationHandler.END

    except Exception as x:
        print(f"Xato bor: {x}")
        update.message.reply_text(text=f"❌ Qayta urinib ko‘ring. Xato: {x}")
        return "Balance"


def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")

    updater = Updater(token=token, use_context=True)
    dp = updater.dispatcher

    # Ro'yxatdan o'tish ConversationHandler
    register_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex(r"^📝 Ro'yxatdan O'tish$"), register),
                      MessageHandler(Filters.regex(r"^💳 Karta qo‘shish$"),register)],
        states={
            'Phone_number': [
                MessageHandler(Filters.contact, phone_number),
                MessageHandler(Filters.text & ~Filters.command, phone_number)
            ],
            'Name': [MessageHandler(Filters.text & ~Filters.command, name)],
            'Carta_type': [MessageHandler(Filters.text & ~Filters.command, card_type)],
            'Carta': [MessageHandler(Filters.text & ~Filters.command, carta)],
            'Balance': [MessageHandler(Filters.text & ~Filters.command, balance)]
        },
        fallbacks=[
            CommandHandler("cancel", cancel),
            MessageHandler(Filters.regex(r'^❌ Cancel$'), cancel)
        ]
    )
    dp.add_handler(register_handler)

    toldirish_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex(r"^💰 Hisobni to'ldirish$"), start_toldirish)],
        states={
            "TOLDIRISH": [MessageHandler(Filters.text & ~Filters.command, hisobni_toldirish)]
        },
        fallbacks=[
            CommandHandler("cancel", cancel),
            MessageHandler(Filters.regex(r'^❌ Cancel$'), cancel)
        ]
    )
    dp.add_handler(toldirish_handler)

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.text("💸 Pul o'tqazish"), pul_otqazish)],
        states={
            KIMGA_OTQAZISH: [MessageHandler(Filters.text & ~Filters.command, kimga_otqazish)],
            MIQDOR_KIRITISH: [MessageHandler(Filters.text & ~Filters.command, miqdor_kiritish)],
        },
        fallbacks=[
            CommandHandler("cancel", cancel),
            MessageHandler(Filters.regex(r'^❌ Cancel$'), cancel)
        ]
    )
    dp.add_handler(conv_handler)

    dp.add_handler(CommandHandler("cancel", cancel), group=0)
    dp.add_handler(MessageHandler(Filters.regex(r'^❌\s*Cancel$'), cancel), group=0)
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.regex(r'^💼\s*Hisobga kirish$'), hisob))
    dp.add_handler(MessageHandler(Filters.text("📊 Balansni tekshirish"), balans))
    dp.add_handler(MessageHandler(Filters.text("📜 To'lovlar tarixi"), tolovlar_tarixi))
    dp.add_handler(MessageHandler(Filters.text("🏠 Asosiy Menu"), main_menu))
    dp.add_handler(MessageHandler(Filters.text("👥 Foydalanuvchilarni ko'rish"), foydalanuvchilarni_korish))
    dp.add_handler(MessageHandler(Filters.text("⬅️ Ortga"), hisob))
    dp.add_handler(MessageHandler(Filters.text("To'liq malumot "), info))
    dp.add_handler(
        MessageHandler(
            Filters.user(user_id=ADMIN_ID) & Filters.regex(r'^/sql\b'),
            sql_query
        ),
        group=10
    )


    logging.debug("Bu DEBUG xabari (faqat tekshiruv uchun).")
    logging.info("Foydalanuvchi kirdi.")
    logging.warning("Xavfli vaziyat yuz berdi!")
    logging.error("Xatolik sodir bo‘ldi!")
    logging.critical("Juda jiddiy xato!!!")

    updater.start_polling()
    updater.idle()
if __name__ == "__main__":
    main()