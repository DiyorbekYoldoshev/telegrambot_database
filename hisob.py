import os
from telegram.ext import CallbackQueryHandler, CommandHandler, MessageHandler, Filters, Updater, ConversationHandler
from telegram import KeyboardButton, ReplyKeyboardMarkup, BotCommand, ChatAction, Update
import sqlite3
from dotenv import load_dotenv

database_path = "tr_bot.db"
load_dotenv()
ADMIN_ID = 1954153232



def get_cancel_keyboard(extra_buttons=None):
    buttons = []
    if extra_buttons:
        buttons.extend(extra_buttons)
    buttons.append([KeyboardButton(text="❌ Cancel")])
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


def start(update, context):
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    update.message.reply_text(text="👋 Assalomu alaykum!\n🤖 Tranzaksiya botga xush kelibsiz!")
    reply_markup = get_cancel_keyboard([
        [KeyboardButton("💼 Hisobga kirish"), KeyboardButton("📝 Ro'yxatdan O'tish")]
    ])
    update.message.reply_text(text="📍 Asosiy Menu", reply_markup=reply_markup)


def cancel(update, context):
    update.message.reply_text(text="❌ Bot to‘xtatildi. \n🔄 Qayta boshlash uchun /start buyrug‘ini yuboring.")
    return ConversationHandler.END


def hisob(update, context):
    user_id = update.effective_user.id

    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name, phone_number, card_type, cart_number FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        name, phone, card_type, card = row
        update.message.reply_text(
            f"📊 <b>Sizning hisobingiz</b>\n\n"
            f"👤 <b>Ism:</b> {name}\n"
            f"📱 <b>Telefon:</b> {phone}\n"
            f"🎫 <b>Telefon:</b> {card_type}\n"
            f"💳 <b>Karta raqami:</b> {card}\n",
            parse_mode="HTML"
        )
    else:
        update.message.reply_text("⚠️ Siz hali ro‘yxatdan o‘tmagansiz.")
        return

    reply_text = "👇 Quyidagilardan birini tanlang:"
    reply_markup = ReplyKeyboardMarkup([
        [KeyboardButton(text="🏠 Asosiy Menu"), KeyboardButton(text="📊 Balansni tekshirish"),
         KeyboardButton(text="To'liq malumot")],
        [KeyboardButton(text="💰 Hisobni to'ldirish"), KeyboardButton(text="📜 To'lovlar tarixi"),
         KeyboardButton(text="💸 Pul o'tqazish")
         ], [KeyboardButton(text="❌ Cancel"), KeyboardButton(text="👥 Foydalanuvchilarni ko'rish")]
    ], resize_keyboard=True)
    update.message.reply_text(text=reply_text, reply_markup=reply_markup)


def info(update, context):
    user_id = update.effective_user.id

    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name, phone_number, card_type, balance, cart_number FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        name, phone, card_type, balance, card = row
        update.message.reply_text(
            f"📊 <b>Sizning hisobingiz</b>\n\n"
            f"👤 <b>Ism:</b> {name}\n"
            f"📱 <b>Telefon:</b> {phone}\n"
            f"🎫 <b>Karta Turi:</b> {card_type}\n"
            f"💳 <b>Karta raqami:</b> {card}\n"
            f"💰 <b>Hisobingiz:</b> {balance} so‘m\n",
            parse_mode="HTML"
        )
    else:
        update.message.reply_text("❌ Siz ro‘yxatdan o‘tmagansiz!")

    reply_text = "👇 Quyidagilardan birini tanlang:"
    reply_markup = ReplyKeyboardMarkup([
        [KeyboardButton(text="🏠 Asosiy Menu"), KeyboardButton(text="📊 Balansni tekshirish"),
         KeyboardButton(text="To'liq malumot")],
        [KeyboardButton(text="💰 Hisobni to'ldirish"), KeyboardButton(text="📜 To'lovlar tarixi"),
         KeyboardButton(text="💸 Pul o'tqazish")
         ], [KeyboardButton(text="❌ Cancel"), KeyboardButton(text="👥 Foydalanuvchilarni ko'rish")]
    ], resize_keyboard=True)
    update.message.reply_text(text=reply_text, reply_markup=reply_markup)


def balans(update, context):
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    conn = sqlite3.connect("tr_bot.db")
    cursor = conn.cursor()
    cursor.execute("select name, balance from users where id = ? ", (update.effective_user.id,))
    reply_text = "🔄 Ma'lumotlar yuklanmoqda..."
    reply_markup = ReplyKeyboardMarkup([
        [KeyboardButton(text="🏠 Menu")]
    ], resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text(text=reply_text, reply_markup=reply_markup)
    result = cursor.fetchone()
    if result:
        name, balance = result
        update.message.reply_text(
            text=f"👤 <b>Ism:</b> {name}\n💰 <b>Hisobingiz:</b> {balance} so‘m",
            parse_mode="HTML"
        )
        reply_text = "👇 Quyidagilardan birini tanlang:"
        reply_markup = ReplyKeyboardMarkup([
            [KeyboardButton(text="🏠 Asosiy Menu"), KeyboardButton(text="📊 Balansni tekshirish"),
             KeyboardButton(text="To'liq malumot")],
            [KeyboardButton(text="💰 Hisobni to'ldirish"), KeyboardButton(text="📜 To'lovlar tarixi"),
             KeyboardButton(text="💸 Pul o'tqazish")
             ], [KeyboardButton(text="❌ Cancel"), KeyboardButton(text="👥 Foydalanuvchilarni ko'rish")]
        ], resize_keyboard=True)
        update.message.reply_text(text=reply_text, reply_markup=reply_markup)

    else:
        update.message.reply_text(text="⚠️ Ma'lumot topilmadi.")

    conn.close()


def start_toldirish(update, context):
    update.message.reply_text("💵 Qancha miqdorda hisobingizni to'ldirmoqchisiz?")
    return "TOLDIRISH"


def hisobni_toldirish(update, context):
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    try:
        miqdor = update.message.text.strip()
        if not miqdor.isdigit():
            update.message.reply_text("🚫 Faqat raqam kiriting.")
            return "TOLDIRISH"

        miqdor = int(miqdor)
        if not (0 < miqdor < 100_000_000):
            update.message.reply_text("🚫 Miqdor 0 va 100 000 000 oralig‘ida bo‘lishi kerak.")
            return "TOLDIRISH"

        user_id = update.effective_user.id
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET balance = balance + ? WHERE id = ?", (miqdor, user_id))
        cursor.execute("SELECT name, balance FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        conn.commit()
        conn.close()

        if row:
            name, balance = row
            update.message.reply_text(
                f"✅ Hisob muvaffaqiyatli to‘ldirildi!\n\n"
                f"👤 <b>Ism:</b> {name}\n"
                f"💸 <b>To‘ldirilgan summa:</b> {miqdor}\n"
                f"💰 <b>Umumiy hisob:</b> {balance}",
                parse_mode="HTML"
            )
            user_id = update.effective_user.id
            username = f"@{update.effective_user.username}" if update.effective_user.username else "Username yo'q"
            if user_id != ADMIN_ID:
                context.bot.send_message(
                    chat_id=ADMIN_ID,
                    text=(
                        f"📢 <b>Foydalanuvchi hisobini to‘ldirdi</b>\n\n"
                        f"👤 <b>Ism:</b> {name}\n"
                        f"📛 <b>Username:</b> {username}\n"
                        f"💸 <b>To‘ldirilgan summa:</b> {miqdor}\n"
                        f"💰 <b>Umumiy balans:</b> {balance}"
                    ),
                    parse_mode="HTML"
                )

            update.message.reply_text("🎉 <b>Muvaffaqiyatli qo‘shildi!</b>", parse_mode="HTML")

            reply_text = "👇 Quyidagilardan birini tanlang:"
            reply_markup = ReplyKeyboardMarkup([
                [KeyboardButton(text="🏠 Asosiy Menu"), KeyboardButton(text="📊 Balansni tekshirish"),
                 KeyboardButton(text="To'liq malumot")],
                [KeyboardButton(text="💰 Hisobni to'ldirish"), KeyboardButton(text="📜 To'lovlar tarixi"),
                 KeyboardButton(text="💸 Pul o'tqazish")
                 ], [KeyboardButton(text="❌ Cancel"), KeyboardButton(text="👥 Foydalanuvchilarni ko'rish")]
            ], resize_keyboard=True)
            update.message.reply_text(text=reply_text, reply_markup=reply_markup)
            return ConversationHandler.END

    except Exception as error:
        print("Xato:", error)
        update.message.reply_text("❌ Xatolik yuz berdi. Qayta urinib ko‘ring.")
        return "TOLDIRISH"


KIMGA_OTQAZISH, MIQDOR_KIRITISH = range(2)


def pul_otqazish(update, context):
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    user_id = update.effective_user.id

    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name, cart_number FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()

    if not result:
        update.message.reply_text("🚫 Siz ro‘yxatdan o‘tmagansiz.")

        return ConversationHandler.END

    context.user_data["from_account_name"] = result[0]
    context.user_data["from_cart_number"] = result[1]
    conn.close()
    update.message.reply_text("👤 Kimga pul o'tqazmoqchisiz?\n✍️ Iltimos, ismni kiriting.")
    return KIMGA_OTQAZISH


def kimga_otqazish(update, context):
    to_account_name = update.message.text.strip()
    context.user_data["to_account_name"] = to_account_name
    from_account_name = context.user_data["from_account_name"]
    if to_account_name == from_account_name:
        update.message.reply_text(text="O'zingizga pul o'tkaza olmaysiz")
        reply_text = "👇 Quyidagilardan birini tanlang:"
        reply_markup = ReplyKeyboardMarkup([
            [KeyboardButton(text="🏠 Asosiy Menu"), KeyboardButton(text="📊 Balansni tekshirish"),
             KeyboardButton(text="To'liq malumot")],
            [KeyboardButton(text="💰 Hisobni to'ldirish"), KeyboardButton(text="📜 To'lovlar tarixi"),
             KeyboardButton(text="💸 Pul o'tqazish")
             ], [KeyboardButton(text="❌ Cancel"), KeyboardButton(text="👥 Foydalanuvchilarni ko'rish")]
        ], resize_keyboard=True)
        update.message.reply_text(text=reply_text, reply_markup=reply_markup)
        return KIMGA_OTQAZISH

    update.message.reply_text("💰 Qancha miqdorda o'tqazmoqchisiz?\n🔢 Raqam kiriting.")
    return MIQDOR_KIRITISH


def miqdor_kiritish(update, context):
    text = update.message.text.strip()
    if not text.isdigit():
        update.message.reply_text("🚫 Faqat raqam kiriting.")
        return MIQDOR_KIRITISH

    amount = int(text)  # foydalanuvchi jo'natmoqchi bo'lgan to'liq summa (so'mda)
    if not (0 < amount < 100_000_000):
        update.message.reply_text("⚠️ Miqdor 0 va 100 000 000 oralig‘ida bo‘lishi kerak.")
        return MIQDOR_KIRITISH

    from_account_name = context.user_data["from_account_name"]
    from_cart_number = context.user_data["from_cart_number"]
    to_account_name = context.user_data["to_account_name"]

    commission_percent = 5  # foiz
    # integer bo'yicha yaxlitlash: komissiya = round(amount * percent / 100)
    commission = int(round(amount * commission_percent / 100.0))
    net = amount - commission

    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    try:
        # qabul qiluvchining karta raqamini olish (ismi bo'yicha — agar mumkin bo'lsa unique tekshir)
        cursor.execute("SELECT cart_number, id FROM users WHERE name = ?", (to_account_name,))
        res = cursor.fetchone()
        if not res:
            update.message.reply_text("❌ Bunday ismli foydalanuvchi topilmadi.")
            conn.close()
            return ConversationHandler.END

        to_cart_number, receiver_id = res

        # jo'natuvchi balansini tekshirish (butun summa bo'yicha)
        cursor.execute("SELECT balance FROM users WHERE cart_number = ?", (from_cart_number,))
        row = cursor.fetchone()
        if not row:
            update.message.reply_text("🚫 Jo'natuvchi hisob topilmadi.")
            conn.close()
            return ConversationHandler.END

        sender_balance = row[0]
        if sender_balance < amount:
            update.message.reply_text("💸 Hisobingizda yetarli mablag‘ yo‘q.")
            conn.close()
            return ConversationHandler.END

        # TRANSAKSIYA: hammasini bir joyda bajarish
        cursor.execute("BEGIN;")

        # (1) tarix yozuvi — bu yerda amount (gross) ni yozyapmiz;
        cursor.execute("""
            INSERT INTO transactions (from_account_name, to_account_name, amount, cart_number)
            VALUES (?, ?, ?, ?)
        """, (from_account_name, to_account_name, amount, from_cart_number))

        # (2) jo'natuvchi balansidan to'liq summa ayirish (amount)
        cursor.execute("UPDATE users SET balance = balance - ? WHERE cart_number = ?", (amount, from_cart_number))

        # (3) qabul qiluvchiga net qo'shish
        cursor.execute("UPDATE users SET balance = balance + ? WHERE cart_number = ?", (net, to_cart_number))

        # (4) admin hisobiga komissiya qo'shish
        cursor.execute("UPDATE users SET balance = balance + ? WHERE id = ?", (commission, ADMIN_ID))

        conn.commit()

        # bildirishnomalar
        context.bot.send_message(
            chat_id=receiver_id,
            text=f"📥 Sizning hisobingizga {from_account_name} dan {net} so‘m pul muvaffaqiyatli o'tkazildi."
        )

        update.message.reply_text(
            f"✅ {amount} so‘mdan {net} so‘m {to_account_name} ga o'tkazildi.\n"
            f"🔸 Komissiya: {commission} so‘m ({commission_percent}%)",
            parse_mode="HTML"
        )

        # adminga ham xabar
        context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"📊 Tranzaksiya: {from_account_name} ➡️ {to_account_name}\n🔸 Gross: {amount} so'm\n🔸 Net: {net} so'm\n🔸 Komissiya: {commission} so'm"
        )

        conn.close()
        return ConversationHandler.END

    except Exception as e:
        conn.rollback()
        conn.close()
        print("Xatolik:", e)
        update.message.reply_text("🚨 Xatolik yuz berdi. Iltimos, keyinroq urinib ko‘ring.")
        return ConversationHandler.END


def main_menu(update, context):
    keyboard = [
        [KeyboardButton("💳 Karta qo‘shish"), KeyboardButton("📊 Balans")],
        [KeyboardButton("📜 To'lovlar tarixi"), KeyboardButton("⬅️ Ortga")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text("Asosiy menyu:", reply_markup=reply_markup)


def tolovlar_tarixi(update, context):
    try:
        user_id = update.effective_user.id

        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        if user_id == ADMIN_ID:
            # Admin uchun - barcha foydalanuvchilar to‘lovlari
            cursor.execute("""
                SELECT id, from_account_name, to_account_name, amount, created_at
                FROM transactions
                ORDER BY created_at DESC
                LIMIT 30
            """)
            records = cursor.fetchall()
            title = "📜 So‘nggi 30 ta barcha foydalanuvchilar to‘lov tarixi:\n\n"
        else:
            from_account_name = context.user_data["from_account_name"]
            # Oddiy foydalanuvchi uchun - faqat o‘ziniki
            cursor.execute("""
                SELECT id, from_account_name, to_account_name, amount, created_at
                FROM transactions
                WHERE from_account_name = ?
                ORDER BY created_at DESC
                LIMIT 30
            """, (from_account_name,))
            records = cursor.fetchall()
            title = "📜 Sizning so‘nggi 30 ta to‘lovlaringiz:\n\n"

        conn.close()

        if not records:
            update.message.reply_text("📭 Sizda to‘lovlar tarixi mavjud emas ❌")
            return

        # Tarixni formatlash
        history = title
        for tr_id, from_acc, to_acc, amount, created_at in records:
            history += (
                f"🆔 ID: {tr_id}\n"
                f"👤 Kimdan: {from_acc}\n"
                f"➡️ Kimga: {to_acc}\n"
                f"💵 Miqdor: {amount} so‘m\n"
                f"⏰ Vaqt: {created_at}\n\n"
            )

        update.message.reply_text(history)

    except Exception as e:
        update.message.reply_text(f"❌ Xato: {e}")


def foydalanuvchilarni_korish(update, context):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM users")
    result = cursor.fetchall()
    conn.close()

    if result:
        text = "📋 Foydalanuvchilar ro‘yxati:\n\n"
        for idx, r in enumerate(result, start=1):
            text += f"{idx}. {r[0]}\n"
        update.message.reply_text(text=text)
    else:
        update.message.reply_text("❌ Hozirda foydalanuvchilar mavjud emas.")


def sql_query(update, context):
    user_id = update.effective_user.id
    if str(user_id) != str(ADMIN_ID):  # faqat admin ishlata oladi
        update.message.reply_text("Sizda bu buyruqdan foydalanishga ruxsat yo‘q ❌")
        return

    try:
        query = update.message.text.replace("/sql ", "").strip()
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.commit()
        conn.close()

        if rows:
            result = "\n".join([str(row) for row in rows])
            update.message.reply_text(f"Natija:\n{result}")
        else:
            update.message.reply_text("✅ So‘rov muvaffaqiyatli bajarildi (natija yo‘q)")
    except Exception as e:
        update.message.reply_text(f"Xato: {e}")
