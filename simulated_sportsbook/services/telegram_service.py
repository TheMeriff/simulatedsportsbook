from datetime import datetime

import requests


class TelegramService:
    def __init__(self):
        pass

    def send_potty_reminder(self):
        acceptable_hours = [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 1, 2]
        now = datetime.utcnow()
        if now.hour in acceptable_hours:
            bot_token = '550737128:AAFfDfWekynT_wxsQuNpynXkBO4xkdr4QNo'
            bot_chatID = '-496578899'

            url = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&text=' + "Does Madeline need to go potty?"

            r = requests.get(url)

            if r.status_code == 200:
                print('telegram message sent successfully')
            else:
                print('big problems in telegram world')
        else:
            print(f'{now.hour}:{now.minute} not in acceptable hours.')
