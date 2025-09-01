from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def send_locations(context, locations, chat_id, message_id=None):
    buttons = []
    for location in locations:
        buttons.append([
            InlineKeyboardButton(
                text=f"{location['city']}",
                callback_data=f"location_{location['location_id']}"
            )
        ])

    buttons.append([
        InlineKeyboardButton(text="⬅️ Back", callback_data="location_back"),
        InlineKeyboardButton(text="❌ Close", callback_data="close")
    ])

    if message_id:
        context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="<b>Choose Locations</b>",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
            parse_mode="HTML"
        )
    else:
        context.bot.send_message(
            chat_id=chat_id,
            text="<b>Choose Locations</b>",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
            parse_mode="HTML"
        )