from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def send_jobs(context, jobs, chat_id, message_id=None):
    keyboard = []
    for job in jobs:
        keyboard.append([
            InlineKeyboardButton(
                text=f"{job['job_title']} ({job['min_salary']} - {job['max_salary']})",
                callback_data=f"job_{job['job_id']}"
            )
        ])

    keyboard.append([InlineKeyboardButton("❌ Close", callback_data="close")
                     ])

    reply_markup = InlineKeyboardMarkup(keyboard)

    if message_id:
        context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="Ishlar ro‘yxati:",
            reply_markup=reply_markup
        )
    else:
        context.bot.send_message(
            chat_id=chat_id,
            text="Ishlar ro‘yxati:",
            reply_markup=reply_markup
        )
