from datetime import date, timedelta

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .models import Company, Marker, Statistic


def sync(ticker):
    def stat_dict(date, func, value):
        return { 'company': company, 'date': date, 'func': func, 'value': value }

    company = Company.get(Company.ticker == ticker)

    daily_timeseries = pull_timeseries(ticker).get('Time Series (Daily)', {})
    rsi_timeseries = pull_rsi(ticker)['Technical Analysis: RSI']  # .get('Technical Analysis: RSI', {})
    macd_timeseries = pull_macd(ticker).get('Technical Analysis: MACD', {})

    data_for_insert = [
        *[stat_dict(date, 'close',     dp['4. close']) for date, dp in daily_timeseries.items()],
        *[stat_dict(date, 'rsi',       dp['RSI']) for date, dp in rsi_timeseries.items()],
        *[stat_dict(date, 'macd_hist', dp['MACD_Hist']) for date, dp in macd_timeseries.items()],
    ]

    Statistic.replace_many(data_for_insert).execute()


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/rsi")
async def rsi(ticker: str, start_date: str, end_date: str):
    company = Company.get(ticker = ticker)
    rsi_data = company.stats.where(Statistic.func == 'rsi',
                                   Statistic.date >= start_date,
                                   Statistic.date < end_date,
                                   )
    return {
        "data": [{
            "date": dp.date,
            "value": dp.value
        } for dp in rsi_data]
    }

@app.get("/macd_hist")
async def macd_hist(ticker: str, start_date: str, end_date: str):
    company = Company.get(ticker = ticker)
    rsi_data = company.stats.where(Statistic.func == 'macd_hist',
                                   Statistic.date >= start_date,
                                   Statistic.date < end_date,
                                   )
    return {
        "data": [{
            "date": dp.date,
            "value": dp.value
        } for dp in rsi_data]
    }

@app.get("/daily_close")
async def daily_close(ticker: str, start_date: str, end_date: str):
    company = Company.get(ticker = ticker)
    rsi_data = company.stats.where(Statistic.func == 'close',
                                   Statistic.date >= start_date,
                                   Statistic.date < end_date,
                                   )
    return {
        "data": [{
            "date": dp.date,
            "value": dp.value
        } for dp in rsi_data]
    }

@app.get("/markers")
async def markers(ticker: str, start_date: str, end_date: str):
    def all_markers(start_date: str, end_date: str):
        marker_data = (Marker.select(Marker.date, Marker.marker_type, Company.ticker)
                       .join(Company)
                       .where(
                           Marker.date >= start_date,
                           Marker.date < end_date,
                       ))
        print(marker_data)
        return marker_data

    def company_markers(ticker: str, start_date: str, end_date: str):
        company = Company.get(ticker = ticker)
        marker_data = (Marker.select(Marker.date, Marker.marker_type, Company.ticker)
                       .join(Company)
                       .where(
                           Marker.company == company,
                           Marker.date >= start_date,
                           Marker.date < end_date,
                       ))
        return marker_data

    if ticker != 'null':
        marker_data = company_markers(ticker, start_date, end_date)
    else:
        marker_data = all_markers(start_date, end_date)

    return {
        "data": [{
            "date": dp.date,
            "marker_type": dp.marker_type,
            "ticker": dp.company.ticker
        } for dp in marker_data]
    }
