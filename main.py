import requests
from datetime import date, timedelta
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
stock_api_key = "your alphavantage key"
news_api_key = "your alphavantage key"
today = date.today()
yesterday = today - timedelta(days=1)
day_before_yesterday = today - timedelta(days=2)


#TODO 1: Use of  https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
stock_url = "https://www.alphavantage.co/query"
stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": stock_api_key
}
response_stock = requests.get(stock_url, params=stock_parameters)
response_stock.raise_for_status()
stock_data = response_stock.json()
close_price_today = float(stock_data["Time Series (Daily)"][f"{yesterday}"]['4. close'])
close_price_yesterday = float(stock_data["Time Series (Daily)"][f"{day_before_yesterday}"]['4. close'])
dif_percent = ((close_price_today / close_price_yesterday) - 1) * 100

up_down = None
if dif_percent > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

#TODO 2: Use of  https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

if dif_percent <= 5 or dif_percent >= 5:
    url_news = "https://newsapi.org/v2/everything"
    news_parameters = {
        "q": STOCK,
        "apiKey": news_api_key
    }
    response_news = requests.get(url_news, params=news_parameters)
    response_news.raise_for_status()
    news_data = response_news.json()
    articles_data = news_data["articles"]
    three_articles = articles_data[:3]
    formated_article = [f"{STOCK}:{up_down}{dif_percent} %\n Headline: {article['title']}. " 
                        f"\n Brief: {article['description']}" for article in three_articles]

#TODO 3: Use of  https://www.twilio.com
# Send a separate message with the percentage change and each article's title and description to your phone number.
account_sid = "your sid from twilio"
auth_token = "auth token from twilio"
client = Client(account_sid, auth_token)
for article in formated_article:
    message = client.messages.create(
                         body=article,
                         from_='twilio number',
                         to='to send number verified from twilio'
                     )
