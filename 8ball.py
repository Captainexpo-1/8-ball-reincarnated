import slack_sdk
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
import os
import openai
from flask import Flask, request
from flask_cors import CORS
from slackeventsapi import SlackEventAdapter
import random
from prompt import Prompt




# Load environment variables
load_dotenv('.env')
slack_token = os.getenv('SLACK_TOKEN')
signing_secret = os.getenv('SIGNING_SECRET')
# set up server + slack stuff
app = Flask(__name__)
client = slack_sdk.WebClient(token=slack_token)
slack_event_adapter = SlackEventAdapter(signing_secret, '/slack/events', app)

openai_client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

postedMSGS = []

announce = True
# set up prompt
prompt = Prompt("./prompt.json")



try:
    if announce:
        client.chat_postMessage(
            channel="#8-ball-reincarnated-testing",
            text="The 8-ball has risen :skull:"
        )
except Exception as e:
    print(e)


def message(payload):
    channel = payload.get('channel')
    print(channel)
    uid = payload.get('user')
    text = payload.get('text')
    msgid = payload.get('client_msg_id')

    text = text.replace('<@U04M46MS56D>', '')
    can_post = True
    for x in postedMSGS:
        if msgid == x:
            can_post = False
        else:
            print('can\'t post. Duplicate')
    if channel != 'C03DNGQA6SY':
        can_post = False
        print('can\'t post. Wrong channel')

    if can_post:
        print(postedMSGS)
        postedMSGS.append(msgid)
        generateAndPostMsg(text, '#8-ball')



def generateAndPostMsg(text, channel):
    try:
        random_system = random.choice([
            "The 8-balls answer is unusually long. :)",
            "The 8-balls answer is unusually perceptive. ;)",
            "The 8-balls answer is unusually incomprehensible. :(",
        ])
        response = openai_client.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages = prompt.get_prompt_with_input(text,random_system),
        )
        result = response.choices[0].message

        print("OPENAI RESPONSE:", response)

        client.chat_postMessage(channel='#8-ball', text=result)
    except Exception as exc:
        client.chat_postMessage(channel='#8-ball', text=f"An error occurred: {exc}")


app = Flask(__name__)
CORS(app)
@app.route("/slack/events",methods=['POST'])
def Test():
    if request.method == 'POST':
        if not (request.args.get('challenge') is None):
            print(request.args.get('challenge'))
            return request.args.get('challenge')
        else:
            print(request.get_json().get('event', {}))
            message(request.get_json().get('event', {}))
            return 'wow!'

    else:
        return '<h1>This is the 8-ball! How are you doing today?</h1><a href="https://www.hackclub.com">Find us here ;)</a>'

def run_server():
    print('running server')
    app.run(host='0.0.0.0', port=os.getenv("PORT"),debug=True)
run_server()    
