from datetime import datetime
from celery.utils.log import get_task_logger

from .celery import app

from .models import Company, Statistic, ExtractStatus
from .alphavantage_extractor import AlphaVantageExtractor

logger = get_task_logger(__name__)


@app.task
def test(i):
    fb = Company.create(name = 'Facebook', ticker = 'FB')
    print(fb)

@app.task
def sync():
    av_extractor = AlphaVantageExtractor(logger = logger)

    try:
        av_extractor.sync_least_recent_company()
    except Exception as exc:
        logger.error(exc)


    # def stat_dict(date, func, value):
    #     return { 'company': company, 'date': date, 'func': func, 'value': value }

    # av = AlphaVantageClient('22TFAC8PEEOZIY3F')

    # company = Company.get_by_id(company_id)
    # logger.info('Starting sync for ' + company.name)

    # # pull new data
    # daily_timeseries = av.pull_daily(company.ticker).get('Time Series (Daily)', {})
    # rsi_timeseries = av.pull_rsi(company.ticker).get('Technical Analysis: RSI', {})
    # macd_timeseries = av.pull_macd(company.ticker).get('Technical Analysis: MACD', {})

    # # insert new data
    # data_for_insert = [
    #     *[stat_dict(date, 'close',     dp['4. close'])  for date, dp in daily_timeseries.items()],
    #     *[stat_dict(date, 'rsi',       dp['RSI'])       for date, dp in rsi_timeseries.items()],
    #     *[stat_dict(date, 'macd_hist', dp['MACD_Hist']) for date, dp in macd_timeseries.items()],
    # ]

    # Statistic.replace_many(data_for_insert).execute()

    # logger.info('Saved data for ' + company.name)
    # logger.info('Updating extract status')
    # logger.info('')

    # # update the extract status
    # extract_status = (company.extract_statuses
    #                     .where(ExtractStatus.extraction_type == 'AlphaVantage')
    #                     .get())
    # extract_status.extracting_now = False
    # extract_status.extracted_until = max(
    #     [datetime.strptime(d, "%Y-%m-%d") for d in daily_timeseries],
    # )
    # extract_status.last_successful_extraction_time = datetime.now()
    # extract_status.save()
