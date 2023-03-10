#!/usr/bin/env python3
import os

import praw
import requests
from json import dumps
import time
from dotenv import load_dotenv

load_dotenv()

# Reddit account information; you cannot delete data for an account you do not have access to.
username = os.environ.get('REDDIT_USERNAME')
password = os.environ.get('REDDIT_PASSWORD')

client_id = os.environ.get('REDDIT_CLIENT_ID')
client_secret = os.environ.get('REDDIT_CLIENT_SECRET')

user_agent = os.environ.get('REDDIT_USER_AGENT', 'centralized mirror for r/publicfreakout')
sub_reddit_name = os.environ.get('REDDIT_SUB_REDDIT_NAME', 'publicfreakout')

# A Mirror Bot Access Token
api_endpoint = "https://api.amirror.link/v1/Link"
api_token = os.environ.get('MIRROR_BOT_ACCESS_TOKEN')

api_header_content = {'Content-Type': 'application/json', 'Authorization': api_token}


def push_link(post_id, mirror_url):
    json_data = {
        "redditPostId": post_id,
        "linkUrl": mirror_url,
        "linkType": "download"
    }

    req = {}

    retries = 0
    retry_limit = 3

    while retries < retry_limit:
        try:
            req = requests.post(api_endpoint, headers=api_header_content, data=dumps(json_data))

            if req.status_code == 200 or req.status_code == 201:
                print("Mirror posted: " + mirror_url)
                break
            else:
                retries += 1
                time.sleep(2)
        except Exception as e:
            print("Mirror API Error: " + str(e))
            retries += 1

        return req.content


def delete_link(post_id, mirror_url):
    json_data = {
        "data": {
            "redditPostId": post_id,
            "url": mirror_url
        }
    }

    req = {}
    try:
        req = requests.delete(api_endpoint, headers=api_header_content, data=json_data)
    except Exception as e:
        print("Mirror API delete error: " + str(e))

    return req.content


def validate(submission):
    return submission and "v.redd.it" in submission.url or "i.imgur.com" in submission.url \
           or ("i.redd.it" in submission.url and str(submission.url).endswith(
        ".gif")) or "gfycat.com" in submission.url or "streamable.com" in submission.url \
           or "giphy.com" in submission.url or "twitter.com" in submission.url


def authenticate():
    print('Authenticating...\n')
    authentication = praw.Reddit(username=username, password=password, client_id=client_id,
                                 client_secret=client_secret,
                                 user_agent=user_agent)
    print(f'Authenticated as {authentication.user.me()}\n')
    return authentication


if __name__ == '__main__':
    try:
        reddit = authenticate()

        print("Successfully authenticated " + username + ". Starting started.")

        for submission in reddit.subreddit(sub_reddit_name).stream.submissions():

            if validate(submission):
                if "twitter.com" in submission.url:
                    url = "https://twitsave.com/info?url=" + submission.url
                    push_link(submission.id, url)
                    continue
                else:
                    url = "https://rapidsave.com" + submission.permalink
                    push_link(submission.id, url)

    except Exception as e:
        print(e)
        pass
