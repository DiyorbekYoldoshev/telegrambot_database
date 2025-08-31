from send_buttons import send_regions,send_jobs
from config import DATABASE
from database import Database

db = Database(DATABASE)

def message_handler(update, context):
    message = update.message.text
    if message == "Regions":
        regions = db.get_all_regions()
        send_regions(context=context, regions=regions, chat_id=update.message.from_user.id)

    elif message == "Jobs":
        jobs = db.get_all_jobs()
        send_jobs(context=context,jobs=jobs,chat_id=update.message.from_user.id)
