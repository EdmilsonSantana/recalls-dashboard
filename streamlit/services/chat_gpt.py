import json
import requests
from dotenv import load_dotenv
import os

load_dotenv()

CHAT_GPT_URL = "https://api.openai.com/v1/completions"


class ChatGPT(object):
    def __init__(self):
        self.header = {
            "Authorization": "Bearer %s" % (os.getenv('CHAT_GPT_API_TOKEN'))
        }

    def ask(self, text):
        data = {
            "model": "text-davinci-003",
            "prompt": text,
            "temperature": 1,
            "max_tokens": 500
        }
        response = requests.post(CHAT_GPT_URL, json=data, headers=self.header)
        return self.process_response(response)

    def process_response(self, response):
        responseContent = response.text
        try:
            return json.loads(responseContent)['choices'][0]['text'].strip() if responseContent else "No response."
        except KeyError:
            return json.loads(responseContent)['error']['message'].strip()
        except Exception:
            return "Unknown error."
