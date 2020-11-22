from datetime import datetime

from .alphavantage_client import AlphaVantageClient
from .models import Company, ExtractStatus, Statistic


class AlphaVantageExtractor:
    def __init__(self, logger):
        self.av = AlphaVantageClient('22TFAC8PEEOZIY3F')
        self.logger = logger

    def sync_least_recent_company(self):
        extract_status = (ExtractStatus.select()
                          .where(ExtractStatus.extraction_type == 'AlphaVantage',
                                 ExtractStatus.extracting_now == False)
                          .order_by(ExtractStatus.extracted_until)
                          .get())
        company = extract_status.company

        extract_status.extracting_now = True
        extract_status.save()

        self.logger.info('Syncing ' + company.name)

        try:
            self.sync(company)
        except Exception as exc:
            self.logger.error(exc)
            extract_status.extracting_now = False
            extract_status.error = str(exc)
            extract_status.save()


    def sync(self, company):
        def stat_dict(date, func, value):
            return { 'company': company, 'date': date, 'func': func, 'value': value }

        self.logger.info('Starting sync for ' + company.name)

        # pull new data
        daily_timeseries = self.av.pull_daily(company.ticker).get('Time Series (Daily)', {})
        rsi_timeseries = self.av.pull_rsi(company.ticker).get('Technical Analysis: RSI', {})
        macd_timeseries = self.av.pull_macd(company.ticker).get('Technical Analysis: MACD', {})

        # insert new data
        data_for_insert = [
            *[stat_dict(date, 'close',     dp['4. close'])  for date, dp in daily_timeseries.items()],
            *[stat_dict(date, 'rsi',       dp['RSI'])       for date, dp in rsi_timeseries.items()],
            *[stat_dict(date, 'macd_hist', dp['MACD_Hist']) for date, dp in macd_timeseries.items()],
        ]

        Statistic.insert_many(data_for_insert).on_conflict('ignore').execute()

        self.logger.info('Saved data for ' + company.name)
        self.logger.info('Updating extract status')
        self.logger.info('')

        # update the extract status
        extract_status = (company.extract_statuses
                          .where(ExtractStatus.extraction_type == 'AlphaVantage')
                          .get())
        extract_status.extracting_now = False
        extract_status.extracted_until = max(
            [datetime.strptime(d, "%Y-%m-%d") for d in daily_timeseries],
        )
        extract_status.last_successful_extraction_time = datetime.now()
        extract_status.save()
