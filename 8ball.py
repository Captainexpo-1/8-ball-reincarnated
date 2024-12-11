import slack_sdk
from slack_sdk.errors import SlackApiError
import os
import openai
from flask import Flask, request
from slackeventsapi import SlackEventAdapter
import random
from prompt import system_prompt

# Load environment variables
from dotenv import load_dotenv
load_dotenv()





def message(payload):
    channel = payload.get('channel')
    print(channel)
    uid = payload.get('user')
    text = payload.get('text')
    msgid = payload.get('client_msg_id')

    text = text.replace('<@U04M46MS56D>', '')
    can_post = msgid not in postedMSGS and channel == 'C03DNGQA6SY'
    if not can_post:
        print('Cannot post')
        return
    
    print(postedMSGS)
    postedMSGS.add(msgid)
    generateAndPostMsg(text, '#8-ball')


def generate_msg(text):
    try:
        new_prompt = system_prompt.copy()
        new_prompt.append({"role":"user","content":text})
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=new_prompt
        )
        print("RETURN:",response.choices[0].message)
        result = response.choices[0].message.content

        print("OPENAI RESPONSE:", response)
        return result
    except Exception as e:
        print(e)
        return "An error occurred: " + str(e)
def generateAndPostMsg(text, channel):
    try:
        result = generate_msg(text)

        client.chat_postMessage(channel='#8-ball', text=result)
    except Exception as exc:
        client.chat_postMessage(channel='#8-ball', text=f"An error occurred: {exc}")


slack_token = os.getenv('SLACK_TOKEN')
signing_secret = os.getenv('SIGNING_SECRET')
openai_api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)

client = slack_sdk.WebClient(token=slack_token)
slack_event_adapter = SlackEventAdapter(signing_secret, '/slack/events', app)

openai_client = openai.OpenAI(api_key=openai_api_key)

postedMSGS = set()
announce = True

@slack_event_adapter.on('message')
def slack_events():
    payload = request.get_json()
    print(payload)
    message(payload)

@slack_event_adapter.on('app_mention')
def app_mention(payload):
    message(payload.get('event'))

def run_server():
    print('running server on port', os.getenv("PORT")) 
     
    app.run(host='0.0.0.0', port=os.getenv("PORT"),debug=True)


if __name__ == "__main__":
    try:
        if announce:
            client.chat_postMessage(
                channel="#8-ball-reincarnated-testing",
                text="The 8-ball has risen :skull:"
            )
    except Exception as e:
        print(e)
     
    run_server()    


