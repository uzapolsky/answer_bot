import random

import vk_api as vk
import os
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType
from dialogflow_anser import detect_intent_texts


def echo(event, vk_api):
    vk_api.messages.send(
        user_id=event.user_id,
        message=detect_intent_texts(
            os.getenv('PROJECT_ID'),
            event.user_id,
            event.text,
            'ru-RU'
        ),
        random_id=random.randint(1,1000)
    )


def main() -> None:
    load_dotenv()
    vk_session = vk.VkApi(token=os.getenv('VK_BOT_TOKEN'))
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api)


if __name__ == '__main__':
    main()