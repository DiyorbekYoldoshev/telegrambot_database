from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def send_employees(context, employees, chat_id, message_id=None):
    buttons = []
    for employee in employees:
        buttons.append([
            InlineKeyboardButton(
                text=f"{employee['first_name']} {employee['last_name']}",
                callback_data=f"employee_{employee['employee_id']}"
            )
        ])
    buttons.append([
        InlineKeyboardButton(text="⬅️ Back", callback_data="job_back"),
        InlineKeyboardButton(text="❌ Close", callback_data="close")
    ])

    reply_markup = InlineKeyboardMarkup(buttons)

    if message_id:
        context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="<b>Choose employees:</b>",
            reply_markup=reply_markup,
            parse_mode="HTML"
        )
    else:
        context.bot.send_message(
            chat_id=chat_id,
            text="<b>Choose employees:</b>",
            reply_markup=reply_markup,
            parse_mode="HTML"
        )