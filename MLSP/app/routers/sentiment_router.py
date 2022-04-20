from typing import Optional
from datetime import date as date, timedelta

from fastapi import APIRouter

from MLSP.app.internal.sentiment_analysis.fin_news_scraper import scrape_finviz
from MLSP.app.internal.sentiment_analysis.twitter_scraper import scrape_hashtag
from MLSP.app.internal.sentiment_analysis.vader_analysis import analyse_sentiment

router = APIRouter(
    prefix="/sentiment",
    responses={404: {"Description": "Couldn't get data, check path and variables are correct"}}
)


@router.get('/twitter')
def twitter_sentiment(hashtag: str, date_start: Optional[date] = date.today() - timedelta(days=1),
                      date_end: Optional[date] = date.today()):

    # Check for hashtag and add if needed
    if not hashtag.startswith("#"):
        hashtag = "#" + hashtag

    tweets = scrape_hashtag(hashtag, date_start, date_end)
    compound_scores, score_per_date = analyse_sentiment(tweets)

    return compound_scores, score_per_date


@router.get('/fin-news')
def financial_news_sentiment(ticker: str):
    finance_news = scrape_finviz(ticker)
    compound_scores, score_per_date = analyse_sentiment(finance_news)

    return compound_scores, score_per_date


@router.get('/combined')
def combined_sentiment(hashtag: str, date_start: Optional[date], date_end: Optional[date]):
    twitter_compound_scores, twitter_score_per_date = twitter_sentiment()
    finance_compound_scores, finance_score_per_date = financial_news_sentiment()

    return twitter_compound_scores, twitter_score_per_date, finance_compound_scores, finance_score_per_date
