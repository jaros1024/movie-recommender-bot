from lib.recommender import Recommender
from lib.bot import Bot
from slackclient import SlackClient
from config import *


def _get_message_details(starter_bot_id, events):
    for event in events:
        if event['type'] == "message" and 'subtype' not in event and event['user'] != starter_bot_id:
            return event['user'], event['channel'], event['text']

    return None


if __name__ == "__main__":
    recommender = Recommender(MOVIES_PATH, CREDITS_PATH)
    slack_client = SlackClient(SLACK_BOT_TOKEN)
    bot = Bot(recommender)

    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        starter_bot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            input = slack_client.rtm_read()
            msg_data = _get_message_details(starter_bot_id, input)
            if msg_data:
                response = bot.process_message(msg_data[0], msg_data[2])
                slack_client.api_call("chat.postMessage", channel=msg_data[1], text=response)
    else:
        print("Connection failed. Exception traceback printed above.")
