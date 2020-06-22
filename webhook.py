import requests
from jotform import JotformAPIClient
import time
import json
import random

class JotformMonitor:

    def __init__(self):
        self.latest = None
        self.entrance_webhook = 'https://discordapp.com/api/webhooks/721531220479049868/9AaNPBSNi3fYt0sL-AJ8M_UGqmS0dRHx_ZEiWDUYOPj8XtfHK8k4ZC0P0ok6eLCz1aP6'
        self.count = 0
        self.tokens = ['17df4208b37eb80324e68805b6bce15a', '83285c23f180db2702c30f7eaba34382', '985a737612e7cdcb5edeae88a5b66c67', 'be70837a6313c19b28226e18a4c2e258', '5834536ae379568cb112b78ef92ca208']
        self.jotform_api = JotformAPIClient(random.choice(self.tokens))

    def load_data(self):
        with open('keys.json', 'r') as f:
            return json.load(f)

    def dump_data(self, data):
        with open('keys.json', 'w') as f:
            return json.dump(data, f)

    def regenerate_auth(self):
        token = self.tokens[self.count]
        if self.tokens.index(token) == len(self.tokens) - 1:
            self.count = 0
        else:
            self.count += 1
        self.jotform_api = JotformAPIClient(token)

    def monitor_keys(self, *, seconds=0, minutes=0, hours=0):
        self.latest = self.jotform_api.get_form_submissions('201360640153038')

        # loop
        while True:
            newest = self.jotform_api.get_form_submissions('201360640153038')
            if newest != self.latest:
                data = self.load_data()
                new_submissions = [submission for submission in newest if submission not in self.latest]
                self.latest = newest
                for submission in new_submissions:
                    if submission['form_id'] == '201360640153038':
                        username = submission['answers']['5']['answer']
                        key = submission['answers']['24']['answer']
                        data[username] = key
                        self.dump_data(data)
                        requests.post(self.entrance_webhook, json={'content': f'username: {username}\nkey: {key}'})
            self.regenerate_auth()
            time.sleep(seconds + minutes*60 + hours*3600)

jotform_monitor = JotformMonitor()
jotform_monitor.monitor_keys(minutes=1)
