from datetime import datetime

import requests


class Logger:
    def __init__(self, tid):
        self.format = '%H:%M:%S'
        self.tid = tid

    def log(self, text, slack=None):
        timestamp = datetime.now().strftime(self.format)
        print('[{}] :: {}'.format(timestamp, text))
        if slack is not None:
            endpoint = 'https://hooks.slack.com/services/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'
            data = {
                "attachments": [
                    {
                        "fallback": "TARGET NES ADDED TO CART",
                        "color": "#36a64f",
                        "author_name": "Thread {}".format(self.tid),
                        "text": text
                    }
                ]
            }
            r = requests.post(
                endpoint,
                json=data,
                headers={'Content-type': 'application/json'}
            )
            try:
                r.raise_for_status()
            except requests.exceptions.HTTPError:
                print r.text
                exit(-1)
