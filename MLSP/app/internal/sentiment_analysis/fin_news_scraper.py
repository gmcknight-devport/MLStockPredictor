from datetime import datetime, timedelta
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import yfinance as yf
from fastapi import HTTPException

finviz_url = "https://finviz.com/quote.ashx?t="


def scrape_finviz(ticker: str):
    processed_data = []

    # Check ticker exists
    t = yf.Ticker(ticker)

    if not t:
        raise HTTPException(status_code=404, detail="Ticker couldn't be found")

    # Create url to search with from ticker
    complete_url = finviz_url + ticker

    # Get HTML response
    request = Request(url=complete_url, headers={'user-agent': 'app'})
    response = urlopen(request)

    # Parse HTML from url
    html = BeautifulSoup(response, 'html')
    ticker_news_data = html.find(id='news-table')

    # Required to find date in scraped data
    now = datetime.now()
    date = None

    # Loop through parsed data to gather timestamps and titles
    for row in ticker_news_data.findAll('tr'):
        title = row.a.text
        timestamp_tag = row.find('td', width='130')

        # Check date exists. Process depending on value.
        if timestamp_tag:
            timestamp_data = timestamp_tag.text.strip()
            parts = timestamp_data.split()
            if len(parts) == 2:
                if 'today' in timestamp_data.lower():
                    date = datetime.strptime(now.strftime('%Y-%m-%d'), '%Y-%m-%d').date()
                else:
                    date_str = timestamp_data.split()[0]
                    date = datetime.strptime(date_str, '%b-%d-%y').date()

        # Check title is relevant to ticker - contains stock name or ticker
        title_str = str(title)
        # if ticker in title_str or short_name in title_str:
        if ticker in title_str:
            processed_data.append([date, title])

    return processed_data
