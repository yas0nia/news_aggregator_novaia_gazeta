

# News aggregator

### Installation:

1. Create `config.py` file with required credentials (see `config_example.py`). This file shoud be in the same folder with all the scripts.

2. Install all required dependecies - `pip install -r requirements.txt`

3. Start `telegram_parser.py`, to authenticate through telethon(https://docs.telethon.dev/en/stable/) and receive `bot.session`, `gazp.session` files required for bot's work.
IMPORTANT: use your telephone number when requested, do NOT use your bot API key as it won't be able to forward messages as a bot, you do it 'through' your account. 

4. Run any parser available or run `python main.py` to start all the parsers
