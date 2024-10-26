from apps.utils.bot import bot_send_message_if_user_offline
from celery_config import celery_app


@celery_app.task
def send_msg_if_offline(message_owner_name: str, text: str, user_tlg_id: int or str):
    bot_send_message_if_user_offline(message_owner_name, text, user_tlg_id)
    return {'owner_name': message_owner_name, 'is_successfully': True}


