import requests
from datetime import datetime, timedelta
from twilio.rest import Client

today = str(datetime.now().date())
yesterday = str(datetime.today().date() - timedelta(days=1))

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API_KEY = YOUR ALPHA ADVANTAGE API KEY

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = YOUR NEWS API KEY
# Twilio Information
auth_token = YOUR TWILIO ACCOUNT AUTH TOKEN
account_sid = YOUR TWILIO ACCOUNT SID

stock_price_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY
}

news_params = {
    "qInTitle": COMPANY_NAME,
    "apiKey": NEWS_API_KEY,
}

stock_response = requests.get(url=STOCK_ENDPOINT, params=stock_price_params)
stock_data = stock_response.json()

today_close = float(stock_data["Time Series (Daily)"][today]["4. close"])
yesterday_close = float(stock_data["Time Series (Daily)"][yesterday]["4. close"])

close_delta = round(today_close - yesterday_close, 2)
day_percent_change = close_delta / yesterday_close * 100

if day_percent_change > 5 or day_percent_change < -5:
    news_response = requests.get(url=NEWS_ENDPOINT, params=news_params)
    news_data = news_response.json()
    for i in range(0, 3):
        headlines = news_data["articles"][i]["title"]
        brief = news_data["articles"][i]["description"]
        if day_percent_change < 0:
            delta_message_input = f"🔻 {day_percent_change}"
        else:
            delta_message_input = f"🔺 {day_percent_change}"

        client = Client(account_sid, auth_token)

        message = client.messages \
            .create(
            body=f"{STOCK}: {delta_message_input}\nHeadline: {headlines}\nBrief: {brief}",
            from_='+15165008122',
            to='+18477705229'
        )
    print(message.status)

