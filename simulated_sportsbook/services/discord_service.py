import requests


class DiscordService:
    def __init__(self):
        self.headers = {
            "Authorization": "Bot NDM2NzY4OTEyNDg3NzQzNDg5.WtmCvw.uoEPrA1J89pM69NnNcE_q2OxokU",
            "Content-Type": "application/json"
        }

    def post_score(self, score_data, channel_id):
        body = {
            "content": score_data
        }
        url = f'https://discordapp.com/api/channels/{channel_id}/messages'
        r = requests.post(headers=self.headers, url=url, json=body)

        if r.status_code == 200:
            data = r.json()
        else:
            print('shit broke')
