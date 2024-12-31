import requests

def send_telegram_message(bot_token: str, chat_id: list, message: str):
    '''
    bot_token: str -> String of the Bot chat you want to update
    chat_id: list -> Take a list of strings that contain the people id's you want to send the message to
    message: str -> String of the message content
    '''
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    for id in chat_id:
        payload = {
            "chat_id": id,
            "text": message
        }
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("TELEGRAM: Message sent successfully!")
        else:
            print(f"TELEGRAM: Failed to send message: {response.text}")