from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd

vader = SentimentIntensityAnalyzer()


def analyse_sentiment(data: object):
    df = pd.DataFrame(data, columns=['date', 'title'])
    df['compound'] = df['title'].apply(
        lambda title: vader.polarity_scores(title)['compound'])

    compound_scores = df[['date', 'compound']]
    score_per_date = compound_scores.groupby('date', as_index=False)['compound'].mean()

    return compound_scores, score_per_date
