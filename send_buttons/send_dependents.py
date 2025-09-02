from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def send_dependents(context, dependents, chat_id, message_id=None):
    buttons = []
    for dependent in dependents:
       buttons.append([
           InlineKeyboardButton(
               text=f"{dependent['first_name']}",
               callback_data=f"dependent_{dependent['dependent_id']}"
           )
       ])
    buttons.append([InlineKeyboardButton(text="⬅️ Back",callback_data="dependent_back"),
                    InlineKeyboardButton(text="❌ Close",callback_data="close")])


    if message_id:
        context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="<b>Choice Dependents</b>",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=buttons
            ),
            parse_mode="HTML"
        )
    else:
        context.bot.send_message(
            chat_id=chat_id,
            text="<b>Choice Dependents</b>",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=buttons
            ),
            parse_mode="HTML"
        )