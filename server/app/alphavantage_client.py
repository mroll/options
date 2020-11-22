import logging
import requests

from .models import DataSource
from .rate_limiter import RateLimiter


logging.basicConfig(level=logging.INFO, format='(%(threadName)-10s) %(message)s')
logger = logging.getLogger(__name__)


class AlphaVantageClient:
    def __init__(self, apikey):
        self.apikey = apikey
        self.baseurl =  'https://www.alphavantage.co'
        self.data_source = DataSource.get(DataSource.name == 'AlphaVantage')
        self.rate_limiter = RateLimiter(
            data_source = self.data_source,
            rules = [
                { "window": 60, "limit": 5, "fail": 'wait' },
                { "window": 60 * 60 * 24, "limit": 500, "fail": 'die' }
            ]
        )

    def _av_get(self, func, symbol, **kwargs):
        def _request():
            url = '{}/query'.format(self.baseurl)

            return requests.get(url, {
                "function": func,
                "symbol": symbol,
                "apikey": self.apikey,
                **kwargs
            })

        return self.rate_limiter.try_request(_request)

    def pull_daily(self, ticker):
        logger.info('Pulling daily data for ' + ticker)
        return self._av_get("TIME_SERIES_DAILY", ticker)

    def pull_rsi(self, ticker):
        logger.info('Pulling rsi data for ' + ticker)
        return self._av_get("RSI", ticker, interval="daily", time_period=14, series_type="close")

    def pull_macd(self, ticker):
        logger.info('Pulling macd_hist data for ' + ticker)
        return self._av_get("MACD", ticker, interval="daily", series_type="close")
