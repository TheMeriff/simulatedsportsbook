import requests

def send_potty_reminder():
    bot_token = '550737128:AAFfDfWekynT_wxsQuNpynXkBO4xkdr4QNo'
    bot_chatID = '-496578899'

    url = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&text=' + "Does Madeline need to go potty?"

    r = requests.get(url)
    if r.status_code == 200:
        print('telegram message sent successfully')
    else:
        print('big problems in telegram world')
