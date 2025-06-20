import os
import requests

def post_to_slack(message):
    slack_url = os.environ.get("SLACK_WEBHOOK_URL")
    if slack_url:
        requests.post(slack_url, json={"text": message})