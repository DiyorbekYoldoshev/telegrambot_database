from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def send_countries(context, countries, chat_id, message_id=None):
    keyboard = []
    for country in countries:
        keyboard.append([
            InlineKeyboardButton(
                text=country['country_name'],
                callback_data=f"country_{country['country_id']}"  # Masalan: country_AR
            )
        ])

    keyboard.append([
        InlineKeyboardButton("⬅️ Back", callback_data="region_back"),
        InlineKeyboardButton("❌ Close", callback_data="close")
    ])

    reply_markup = InlineKeyboardMarkup(keyboard)

    if message_id:
        context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="🌍 Countries:",
            reply_markup=reply_markup
        )
    else:
        context.bot.send_message(
            chat_id=chat_id,
            text="🌍 Countries:",
            reply_markup=reply_markup
        )