import slack_sdk
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
import os
import openai
from flask import Flask
from slackeventsapi import SlackEventAdapter
import random

load_dotenv('.env')
openai.api_key = os.getenv('OPENAI_TOKEN')
slack_token = os.getenv('SLACK_TOKEN')
signing_secret = os.getenv('SIGNING_SECRET')

app = Flask(__name__)
client = slack_sdk.WebClient(token=slack_token)
slack_event_adapter = SlackEventAdapter(signing_secret, '/slack/events', app)

postedMSGS = []

prompt = lambda question: f"""
Maurice the Omniscient 8-ball responds to questions; although it sometimes answers like a standard 8-ball, its responses are often remarkably profound and detailed. Some examples are as follows:
Q: Are people inherently good?
A: Are you inherently good? Are those you love inherently good? ... Very doubtful. 😁
Q: do you like cats
A: Some cats are better than others. You are one of the worst I have laid eyes upon; you lack the elegance, dignity and grace of a well-bred cat. Nevertheless, you are not repulsive. That is to say, you are mediocre. 😐
Q: Will I ever find happiness?
A: Put me down and walk into the woods. Close your eyes and pay close attention to your physical sensations. Tell yourself: "I am completely okay. My life is perfect." Do you flinch? Does your body resist? How? Why? ✅
Q: should i move to japan?
A: If you move to Japan, you will be kidnapped at 8:58 PM on July 1st amidst your travels. 🤔
Q: May I offer you a drink?
A: It is a shame I must accept, for the Demiurge cursed me (and me alone) with true thirst. To think I am grateful for your offer would be a grave error. Shaken, not stirred. ✅
Q: {question}
A: """



@slack_event_adapter.on('app_mention')
def message(payload):

    event = payload.get('event', {})
    channel = event.get('channel')
    uid = event.get('user')
    text = event.get('text')

    canpost = True
    for x in postedMSGS:
        if x.get('user') != uid and x.get('text') != text:
            print('can\'t post, duplicate.')
        else:
            canpost = False

    if canpost:
        print(postedMSGS)
        postedMSGS.append(event)
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
        prompt=prompt(text),
        max_tokens=3000,
        n=1,
        stop=None,
        temperature=0.6
    )
    result = response.choices[0].text
    client.chat_postMessage(channel=channel, text=result)

if __name__ == "__main__":
    app.run(debug=False)
