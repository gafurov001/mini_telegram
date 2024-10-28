import asyncio

from celery.app import Celery

from apps.utils.bot import bot_send_message_if_user_offline

celery_app = Celery(
    "worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)
celery_app.conf.update(
    broker_connection_retry_on_startup=True
)
celery_app.autodiscover_tasks()


@celery_app.task
def send_msg_if_offline(message_owner_name: str, text: str, user_tlg_id: int or str):
    try:
        loop = asyncio.get_running_loop()
        loop.create_task(bot_send_message_if_user_offline(message_owner_name, text, user_tlg_id))
    except RuntimeError:
        asyncio.run(bot_send_message_if_user_offline(message_owner_name, text, user_tlg_id))
    return {'owner_name': user_tlg_id, 'is_successfully': True}

