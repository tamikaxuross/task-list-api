import os
import requests

def post_to_slack(message):
    slack_token = os.environ.get("SLACK_BOT_TOKEN")
    slack_channel = os.environ.get("SLACK_CHANNEL_ID")

    if not slack_token or not slack_channel:
        return

    headers = {
        "Authorization": f"Bearer {slack_token}",
        "Content-Type": "application/json"
    }

    slack_message = {
        "channel": slack_channel,
        "text": message
    }

    requests.post("https://slack.com/api/chat.postMessage", json=slack_message, headers=headers)