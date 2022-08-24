import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter

## Declaring Environment Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path = env_path)

# Flask Var Config
app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(os.environ['SIGN_IN_SECRET'],'/slack/events', app)
# Slack Client Init

client = slack.WebClient(token = os.environ['SLACK_TOKEN'])
BOT_ID = client.api_call("auth.test")['user_id']



# Annotation Funcs

@slack_events_adapter.on('message')
def message(payLoad):
    event = payLoad.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
    
    if BOT_ID != user_id:
        client.chat_postMessage(channel = channel_id, text = text)
   

if __name__ == '__main__':
    app.run(debug = True, port = 5002)