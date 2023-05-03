import requests
from config import api_id, api_hash, gazp_chat_id, bot_token

def send_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
        "disable_notification": False,
    }
    response = requests.post(url, data=payload)
    return response.json()

if __name__ == "__main__":
    api_token = bot_token
    channel_id = gazp_chat_id    
    message_text = "This is a test message from my bot."

    result = send_message(api_token, channel_id, message_text)
    print(result)
