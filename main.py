import slack_sdk
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
import os
import openai
from flask import Flask
from slackeventsapi import SlackEventAdapter

load_dotenv('.env')
openai.api_key = os.getenv('OPENAI_TOKEN')
slack_token = os.getenv('SLACK_TOKEN')
signing_secret = os.getenv('SIGNING_SECRET')

app = Flask(__name__)
client = slack_sdk.WebClient(token=slack_token)
slack_event_adapter = SlackEventAdapter(signing_secret, '/slack/events', app)


@slack_event_adapter.on('app_mention')
def message(payload):

    event = payload.get('event', {})
    channel = event.get('channel')
    uid = event.get('user')
    text = event.get('text')
    generateAndPostMsg(text, uid, channel)


try:
    client.chat_postMessage(
        channel="#8-ball-reincarnated-testing",
        text="8-ball has risen :skull:"
    )
except SlackApiError as e:
    print(e)


def generateAndPostMsg(text, userid, channel):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=text,
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.5
    )
    result = response.choices[0].text
    client.chat_postMessage(channel=channel, text=result)

if __name__ == "__main__":
    app.run(debug=False)
