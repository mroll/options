import sys
import time

import requests
from models import Company, Statistic
from alphavantage import AlphaVantage


av = AlphaVantage('22TFAC8PEEOZIY3F')

sleeptime = 60 / 5 + 2

def sync(company):
    def stat_dict(date, func, value):
        return { 'company': company, 'date': date, 'func': func, 'value': value }

    daily_timeseries = av.pull_daily(company.ticker).get('Time Series (Daily)', {})
    print('daily data points: ', len(daily_timeseries))
    time.sleep(sleeptime)

    rsi_timeseries = av.pull_rsi(company.ticker).get('Technical Analysis: RSI', {})
    print('rsi data points: ', len(rsi_timeseries))
    time.sleep(sleeptime)

    macd_timeseries = av.pull_macd(company.ticker).get('Technical Analysis: MACD', {})
    print('macd data points: ', len(macd_timeseries))
    time.sleep(sleeptime)

    print()

    data_for_insert = [
        *[stat_dict(date, 'close',     dp['4. close'])  for date, dp in daily_timeseries.items()],
        *[stat_dict(date, 'rsi',       dp['RSI'])       for date, dp in rsi_timeseries.items()],
        *[stat_dict(date, 'macd_hist', dp['MACD_Hist']) for date, dp in macd_timeseries.items()],
    ]

    Statistic.replace_many(data_for_insert).execute()


if len(sys.argv) > 1:
    company = Company.get(ticker = sys.argv[1])
    sync(company)
else:
    companies = Company.select()

    for company in companies:
        print("syncing {} ({})".format(company.name, company.ticker))
        sync(company)

        time.sleep(5)
