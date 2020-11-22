from concurrent.futures import ThreadPoolExecutor
import schedule

from .alphavantage_extractor import AlphaVantageExtractor


pool = ThreadPoolExecutor(3)

av_extractor = AlphaVantageExtractor(pool, schedule)
av_extractor.start()
