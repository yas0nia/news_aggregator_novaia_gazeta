

# News aggregator

### Installation:

1. Clone this repository and `cd` to the its folder. 

2. Create `config.py` file with required credentials (see `config_example.py`). This file shoud be in the same folder with all the scripts.

3. Install all required dependecies - `pip install -r requirements.txt`

4. Start `telegram_parser.py`, to authenticate through telethon(https://docs.telethon.dev/en/stable/) and receive `bot.session`, `gazp.session` files required for bot's work.

IMPORTANT: use your telephone number when requested, do NOT use your bot API key as it won't be able to forward messages as a bot, you do it 'through' your account. 

5. Run any parser available or run `python main.py` to start all the parsers

### Running a Docker image

1. Make sure Docker is installed on your computer if you use Windows or MacOS.

2. Clone repository and `cd` to the its folder.

3. Create `config.py` file with required credentials (see `config_example.py`). This file shoud be in the same folder with all the scripts.

4. Run `docker build --tag dockerbot .` to build an image.

5. After that, run `docker run -it dockerbot`. IMPORTANT: use your telephone number when requested, do NOT use your bot API key as it won't be able to forward messages as a bot, you do it 'through' your account.
