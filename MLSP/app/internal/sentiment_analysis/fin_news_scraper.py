from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

finviz_url = "https://finviz.com/quote.ashx?t="


def scrape_finviz(ticker):
    processed_data = []

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

        if len(timestamp_data) == 1:
            time = timestamp_data[0]
        else:
            date = timestamp_data[0]
            time = timestamp_data[1]
        processed_data.append([date, time, title])
