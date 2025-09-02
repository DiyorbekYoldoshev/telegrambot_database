from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def send_locations(context, locations, chat_id, message_id=None):
    keyboard = []
    for location in locations:
        address = location.get('street_address', 'N/A')
        city = location.get('city', 'N/A')
        keyboard.append([
            InlineKeyboardButton(
                text=f"{address}, {city}",
                callback_data=f"location_{location['location_id']}"
            )
        ])

    keyboard.append([
        InlineKeyboardButton("⬅️ Back", callback_data="location_back"),
        InlineKeyboardButton("❌ Close", callback_data="close")
    ])

    reply_markup = InlineKeyboardMarkup(keyboard)

    if message_id:
        context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="📍 Locations:",
            reply_markup=reply_markup
        )
    else:
        context.bot.send_message(
            chat_id=chat_id,
            text="📍 Locations:",
            reply_markup=reply_markup
        )