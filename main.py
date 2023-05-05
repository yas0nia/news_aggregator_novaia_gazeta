import httpx
import asyncio
import logging
from collections import deque
from telethon import TelegramClient

from telegram_parser import telegram_parser
from rss_parser import rss_parser
from utils import create_logger, get_history, send_error_message
from config import api_id, api_hash, gazp_chat_id, bot_token


###########################
# Add any channel you want to parse

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

rss_channels = {
    '47news': 'https://47news.ru/rss/',
    'bloknot': 'https://bloknot.ru/rss.xml',
    'sakhaday': 'https://sakhaday.ru/feed/',
    'nozh': 'https://knife.media/feed/',
    'kedr': 'https://kedr.media/feed',
    'stolica-s': 'https://stolica-s.su/feed',
}


def check_pattern_func(text):
    words = text.lower().split()

    keywords = [
        'взрыв',
        'война',    
        'Донецк',   
        'насил', 
        'пожар',
        'полиц',
        'протест',
        'смерт',
        'теракт',
        'убий',
        'убит',
        'жесток',
        'украин'
    ]

    for word in words:
        for key in keywords:
            if key in word:
                return True

    return False


###########################
# Troubleshooting duplicate posts

# key to search for duplicate posts
n_test_chars = 50

# Amount of already published posts to check for duplicates
amount_messages = 50

# The queue of already published posts
posted_q = deque(maxlen=amount_messages)

# +/- The interval in seconds for making a request to the rss channel
timeout = 120

###########################


logger = create_logger('gazp')
logger.info('Start...')

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

tele_logger = create_logger('telethon', level=logging.ERROR)

bot = TelegramClient('bot', api_id, api_hash,
                     base_logger=tele_logger, loop=loop)
bot.start(bot_token=bot_token)


async def send_message_func(text):
    await bot.send_message(entity=gazp_chat_id,
                           parse_mode='html', link_preview=False, message=text)

    logger.info(text)


client = telegram_parser('gazp', api_id, api_hash, telegram_channels, gazp_chat_id, posted_q,
                         n_test_chars, check_pattern_func, tele_logger, loop)

history = loop.run_until_complete(get_history(client, gazp_chat_id,
                                              n_test_chars, amount_messages))

posted_q.extend(history)

httpx_client = httpx.AsyncClient()

for source, rss_link in rss_channels.items():

    # https://docs.python-guide.org/writing/gotchas/#late-binding-closures
    async def wrapper(source, rss_link):
        try:
            await rss_parser(httpx_client, source, rss_link, posted_q,
                             n_test_chars, timeout, check_pattern_func,
                             send_message_func, logger)
        except Exception as e:
            message = f'&#9888; ERROR: {source} parser is down! \n{e}'
            await send_error_message(message, bot_token, gazp_chat_id, logger)

    loop.create_task(wrapper(source, rss_link))



try:
    client.run_until_disconnected()

except Exception as e:
    message = f'&#9888; ERROR: telegram parser (all parsers) is down! \n{e}'
    loop.run_until_complete(send_error_message(message, bot_token,
                                               gazp_chat_id, logger))
finally:
    loop.run_until_complete(httpx_client.aclose())
    loop.close()
