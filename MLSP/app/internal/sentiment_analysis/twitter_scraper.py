from datetime import date as date, timedelta
from typing import Optional
import re

import snscrape.modules.twitter as scraper
from fastapi import HTTPException


# Scrape tweets for a day by default
# Scrape for a few days - day at a time
def scrape_hashtag(hashtag: str, date_start: Optional[date] = date.today() - timedelta(days=1),
                   date_end: Optional[date] = date.today()):
    scraped_tweets = []

    # Number to scrape
    number_tweets = 50

    # Complete search string
    search_str = hashtag + " since:" + date_start.strftime("%Y-%m-%d") + " until:" + date_end.strftime("%Y-%m-%d")

    # Reduce number of tweets to return per day depending on amount
    if (date_end - date_start).days > 10:
        number_tweets = 15
    elif (date_end - date_start).days > 6:
        number_tweets = 25
    elif (date_end - date_start).days > 4:
        number_tweets = 40

    # Outer loop through days
    while date_start < date_end:

        # Loop through top tweets based on search string
        for i, tweet in enumerate(scraper.TwitterSearchScraper(search_str, top=True).get_items()):
            if i >= number_tweets:
                break

            # Clean and append tweet data
            cleaned_tweet = clean_tweet(tweet.content)
            curr_tweet = (tweet.date.strftime("%Y/%m/%d"), cleaned_tweet)
            scraped_tweets.append(curr_tweet)

        date_start += timedelta(days=1)

    # Raise exception if no tweets are found
    if not scraped_tweets:
        raise HTTPException(status_code=404, detail="No tweets found")

    return scraped_tweets


def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+) | "
                           "([^0-9A-Za-z \t]) | "
                           "(\w+:\ / \ / \S+) | "
                           "(#[A-Za-z0-9_]+) | "
                           "(rhttp\S+) | "
                           "(rwww.\S+) | "
                           "([()!?,]) | "
                           "(\[.*?\])", " ", tweet).split())
