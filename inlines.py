from send_buttons import send_countries, send_regions, send_jobs, send_employees, send_locations
from database import Database

db = Database("sample-database.db")


def inline_handler(update, context):
    query = update.callback_query
    data_sp = str(query.data).split("_")
    chat_id = query.message.chat.id

    if data_sp[0] == "region":
        if data_sp[1].isdigit():
            countries = db.get_countries_by_region(int(data_sp[1]))
            send_countries(context=context, countries=countries, chat_id=chat_id,
                           message_id=query.message.message_id)
        elif data_sp[1] == 'back':
            regions = db.get_all_regions()
            send_regions(context=context, regions=regions, chat_id=chat_id,
                         message_id=query.message.message_id)

    elif data_sp[0] == "job":
        if data_sp[1].isdigit():
            employees = db.get_employees_by_job(int(data_sp[1]))
            send_employees(context=context, employees=employees, chat_id=chat_id,
                           message_id=query.message.message_id)

        elif data_sp[1] == 'back':
            jobs = db.get_all_jobs()
            send_jobs(context=context, jobs=jobs, chat_id=chat_id,
                      message_id=query.message.message_id)

    elif data_sp[0] == "country":

        if data_sp[0] == 'location':
            locations = db.get_all_locations(int(data_sp[1]))
            send_locations(context=context, locations=locations, chat_id=chat_id,
                       message_id=query.message.message_id)

    elif data_sp[0] == "employee":
        pass
    elif data_sp[0] == "close":
        query.message.edit_text(text="🕓", reply_markup=None)
        context.bot.delete_message(chat_id=chat_id, message_id=query.message.message_id)
