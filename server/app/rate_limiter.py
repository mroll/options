from datetime import datetime, timedelta
import logging, time

from .models import RequestLog

logging.basicConfig(level=logging.INFO, format='(%(threadName)-10s) %(message)s')
logger = logging.getLogger(__name__)


class RateLimiter:
    def __init__(self, data_source, rules):
        self.data_source = data_source
        self.rules = rules

    def _pass(self, rule):
        window_start = datetime.now() - timedelta(seconds=rule['window'])
        requests_in_window = (RequestLog.select()
                              .where(RequestLog.data_source == self.data_source,
                                     RequestLog.request_time >= window_start)
                              .count())
        return requests_in_window < rule['limit']

    def _wait_to_pass(self, rule):
        window_start = datetime.now() - timedelta(seconds=rule['window'])
        first_window_request = (RequestLog.select()
                                .where(RequestLog.request_time >= window_start)
                                .order_by(RequestLog.request_time)
                                .get())
        wait_time = (first_window_request.request_time - window_start).seconds
        logger.info('Waiting {}s'.format(wait_time))
        time.sleep(wait_time)

    def try_request(self, make_request):
        for rule in self.rules:
            if not self._pass(rule):
                logger.info('Failed rate limit check')
                if rule['fail'] == 'wait':
                    self._wait_to_pass(rule)
                elif rule['fail'] == 'die':
                    logger.info('Dying')
                    return

        request_time = datetime.now()
        response = make_request()
        RequestLog.create(
            data_source = self.data_source,
            request_time = request_time,
            url = response.url
        )

        return response.json()
