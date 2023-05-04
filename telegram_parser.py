from collections import deque
from telethon import TelegramClient, events
from config import api_id, api_hash, gazp_chat_id


def telegram_parser(session, api_id, api_hash, telegram_channels, gazp_chat_id, posted_q,
                    n_test_chars=50, check_pattern_func=None, logger=None, loop=None):

    telegram_channels_links = list(telegram_channels.values())

    client = TelegramClient(session, api_id, api_hash,
                            base_logger=logger, loop=loop)
    client.start()
    print('Telegram parser started')
    @client.on(events.NewMessage(chats=telegram_channels_links))
    async def handler(event):
        print('New message')
        if event.raw_text == '':
            return

        news_text = ' '.join(event.raw_text.split('\n')[:2])
        print(news_text)

        if not (check_pattern_func is None):
            if not check_pattern_func(news_text):
                return

        head = news_text[:n_test_chars].strip()

        if head in posted_q:
            return

        else:
            await event.message.forward_to(gazp_chat_id)
       
        posted_q.appendleft(head)

    return client


if __name__ == "__main__":

    telegram_channels = {
        1052226869: '@fontankaspb',
        1109634603: '@news161ru',
        1096776982: '@ngs_news',
        1049795479: '@e1_news',
        1125426287: '@news_72ru',
        1056054957: '@ngs24_krsk',
        1121885240: '@newsv1',
        1428490399: '@ufa1news',
        1149575016: '@news63ru',
        1288401875: '@news_93_ru',
        1668724834: '@arh_29ru',
        1154377528: '@ircity_ru',
        1727657508: '@news116ru',
        1783879034: '@ngs42',
        1690565826: '@kurgan_45_RU',
        1080833375: '@nn_ru',
        1135152118: '@ngs55news',
        1142964467: '@news59ru',
        1734699153: '@sochi1news',
        1547459883: '@news_86ru',
        1119067534: '@news_74ru',
        1003897601: '@chitaru75',
        1143857056: '@news76',
        1038402501: '@kommersant',
        1806946093: '@breakingNews27',
        1862902168: '@imsocrazyfrog',
    }

    posted_q = deque(maxlen=20)

    client = telegram_parser('gazp', api_id, api_hash, telegram_channels,  gazp_chat_id, posted_q)

    client.run_until_disconnected()