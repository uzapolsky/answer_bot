import logging
import os
import random

import telegram
import vk_api as vk
from dotenv import load_dotenv
from vk_api.longpoll import VkEventType, VkLongPoll

from dialogflow_answer import detect_intent_texts
from logger import TelegramLogsHandler

logger = logging.getLogger(__name__)


def send_message(event, vk_api):
    is_fallback, message = detect_intent_texts(
        os.getenv('PROJECT_ID'),
        event.user_id,
        event.text,
        'ru-RU'
    )
    if not is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=message,
            random_id=random.randint(1,1000)
        )


def main() -> None:
    load_dotenv()
    log_bot = telegram.Bot(token=os.getenv('LOG_BOT_TOKEN'))
    
    logger.setLevel(logging.WARNING)
    logger.addHandler(TelegramLogsHandler(log_bot, os.getenv('LOG_CHAT_ID')))
    vk_session = vk.VkApi(token=os.getenv('VK_BOT_TOKEN'))
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            try:
                send_message(event, vk_api)
            except Exception:
                logger.exception('VK bot error')


if __name__ == '__main__':
    main()
