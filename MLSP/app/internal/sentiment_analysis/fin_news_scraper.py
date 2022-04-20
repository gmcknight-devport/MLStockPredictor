from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import yfinance as yf
from fastapi import HTTPException

finviz_url = "https://finviz.com/quote.ashx?t="


def scrape_finviz(ticker: str):
    processed_data = []

    # Check ticker exists
    t = yf.Ticker(ticker)

    # Get short name from ticker and remove unnecessary parts
    try:
        stock_name = t.info['shortName']
        first_split = stock_name.split(' ')
        stock_name = first_split[0].split('.')
        short_name = stock_name[0]
    except KeyError:
        raise HTTPException(status_code=404, detail="Ticker couldn't be found")

    # Create url to search with from ticker
    complete_url = finviz_url + ticker

    # Get HTML response
    request = Request(url=complete_url, headers={'user-agent': 'app'})
    response = urlopen(request)

    # Parse HTML from url
    html = BeautifulSoup(response, 'html')
    ticker_news_data = html.find(id='news-table')

    # Loop through parsed data to gather timestamps and titles
    for row in ticker_news_data.findAll('tr'):
        title = row.a.text
        timestamp_data = row.td.text.split(' ')

        # Get date for each title
        if not len(timestamp_data) == 1:
            date = timestamp_data[0]

        # Check title is relevant to ticker - contains stock name or ticker
        title_str = str(title)
        if ticker in title_str or short_name in title_str:
            processed_data.append([date, title])

    return processed_data
