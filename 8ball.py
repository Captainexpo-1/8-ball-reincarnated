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
slack_event_adapter = SlackEventAdapter(signing_secret, '/mentions', app)

postedMSGS = []

announce = False

prompt = lambda question: f"""
Maurice the Omniscient 8-ball responds to questions; although it sometimes answers like a standard 8-ball, its responses are often remarkably profound and detailed.
(if the answer is in a different language, always add a translation in parentheses at the bottom of the response) 
Some examples are as follows:
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
{"(8-ball's answer is unusually intricate :)" if random.random() < 0.3 else "(8-ball's answer is unusually perceptive :)"}
A: """


@slack_event_adapter.on('app_mention')
def message(payload):
    event = payload.get('event', {})
    channel = event.get('channel')
    uid = event.get('user')
    text = event.get('text')

    can_post = True
    for x in postedMSGS:
        if event.get('client_msg_id') == x:
            can_post = False

    if can_post:
        print(postedMSGS)
        postedMSGS.append(event.get('client_msg_id'))
        generateAndPostMsg(text, uid, channel)
    else:
        print('can\'t post, duplicate.')


try:
    if announce:
        client.chat_postMessage(
            channel="#8-ball",
            text="8-ball has risen :skull:"
        )
except SlackApiError as e:
    print(e)


def generateAndPostMsg(text, userid, channel):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt(text) ,
            max_tokens=3000,
            n=1,
            stop=None,
            temperature=1
        )
        result = response.choices[0].text
        client.chat_postMessage(channel=channel, text=result)
    except Exception as exc:
        client.chat_postMessage(channel=channel, text=f"An error occurred: {exc}")


app = Flask(__name__)
@app.route("/")
def hello_world():
    return "<p>BINGGGGG</p>"
def run_server():
    app.run(host='127.0.0.1', port=os.getenv("$PORT"))
run_server()