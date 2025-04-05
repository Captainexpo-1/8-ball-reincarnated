import slack_sdk
import os
import openai
from flask import Flask
from slackeventsapi import SlackEventAdapter
from prompt import Prompt
import re
from typing import Dict, Any

from dotenv import load_dotenv
load_dotenv(override=True)

def message(payload: Dict[str, Any]) -> None:
    channel: str = payload.get('channel')
    print(channel)
    #uid = payload.get('user')
    text: str = payload.get('text')
    msgid: str = payload.get('client_msg_id')

    text = re.sub(r'<@.+>', '', text)
    can_post: bool = msgid not in postedMSGS
    if not can_post:
        print('Cannot post')
        return
    
    #print(postedMSGS)
    postedMSGS.add(msgid)
    generateAndPostMsg(text, channel=channel)


def generate_msg(text: str) -> str:
    try:
        p = Prompt()
        new_prompt = p.get_prompt_with_input(text)
        new_prompt.append({"role":"user","content":text})
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=new_prompt,
            response_format={
                "type": "text"
            },
            temperature=1.4,
            max_tokens=256,
            top_p=0.54,
            frequency_penalty=2,
            presence_penalty=0
        )
        print("RETURN:",response.choices[0].message)
        result: str = response.choices[0].message.content

        print("OPENAI RESPONSE:", response)
        return result
    except Exception as e:
        print(e)
        return "An error occurred: " + str(e)

def generateAndPostMsg(text: str, channel: str) -> None:
    try:
        result: str = generate_msg(text)
        client.chat_postMessage(channel=channel, text=result)
    except Exception as exc:
        client.chat_postMessage(channel=channel, text="An error occurred: " + str(exc))


slack_token: str = os.getenv('SLACK_TOKEN')
signing_secret: str = os.getenv('SIGNING_SECRET')
openai_api_key: str = os.getenv('OPENAI_API_KEY')

app: Flask = Flask(__name__)

client: slack_sdk.WebClient = slack_sdk.WebClient(token=slack_token)
slack_event_adapter: SlackEventAdapter = SlackEventAdapter(signing_secret, '/slack/events', app)

openai_client: openai.OpenAI = openai.OpenAI(api_key=openai_api_key)

postedMSGS: set = set()
announce: bool = True


@slack_event_adapter.on('app_mention')
def app_mention(payload: Dict[str, Any]) -> None:
    message(payload.get('event'))

def run_server() -> None:
    print('running server on port', os.getenv("PORT")) 
    env: str = os.getenv('ENV')
    use_debug: bool = env == 'development'

    app.run(host='0.0.0.0', port=os.getenv("PORT"),debug=use_debug)


if __name__ == "__main__":
    try:
        if announce:
            client.chat_postMessage(
                channel=os.environ['STATUS_CHANNEL'],
                text="The 8-ball has risen :skull:"
            )
    except Exception as e:
        print(e)
     
    run_server()
