from .alphavantage_client import AlphaVantageClient
from .models import Company, Statistic


class AlphaVantageExtractor:
    def __init__(self, pool, schedule):
        self.av = AlphaVantage(AV_API_KEY)
        self.pool = pool
        self.schedule = schedule

    def start(self):
        self.schedule.every(1).minutes.do(self.sync_least_recent_company)

    def sync_least_recent_company(self):
        extract_status = (ExtractStatus.select()
                          .where(ExtractStatus.extraction_type == 'AlphaVantage')
                          .order_by(ExtractStatus.extracted_until)
                          .get())
        self.pool.submit(self.sync, (extract_status.company,))

    def sync(self, company):
        def stat_dict(date, func, value):
            return { 'company': company, 'date': date, 'func': func, 'value': value }

        daily_timeseries = self.av.pull_daily(company.ticker).get('Time Series (Daily)', {})
        rsi_timeseries = self.av.pull_rsi(company.ticker).get('Technical Analysis: RSI', {})
        macd_timeseries = self.av.pull_macd(company.ticker).get('Technical Analysis: MACD', {})

        data_for_insert = [
            *[stat_dict(date, 'close',     dp['4. close'])  for date, dp in daily_timeseries.items()],
            *[stat_dict(date, 'rsi',       dp['RSI'])       for date, dp in rsi_timeseries.items()],
            *[stat_dict(date, 'macd_hist', dp['MACD_Hist']) for date, dp in macd_timeseries.items()],
        ]

        Statistic.replace_many(data_for_insert).execute()
