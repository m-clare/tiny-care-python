import os
import re
import emoji
import twitter
from dotenv import load_dotenv

load_dotenv('./assets/mclare.env')


def strip_emoji(text):
    new_text = re.sub(emoji.get_emoji_regexp(), r"", text)
    return new_text


def get_recent_care_tweet():
    TTC_BOT = os.getenv("TTC_BOT")
    TTC_CONSUMER_KEY = os.getenv("TTC_CONSUMER_KEY")
    TTC_CONSUMER_SECRET = os.getenv("TTC_CONSUMER_SECRET")

    twit = twitter.Api(consumer_key=TTC_CONSUMER_KEY,
                       consumer_secret=TTC_CONSUMER_SECRET,
                       application_only_auth=True)

    recent_tweet = twit.GetUserTimeline(screen_name=TTC_BOT)[0].text.strip()
    recent_tweet = strip_emoji(recent_tweet)
    return recent_tweet
