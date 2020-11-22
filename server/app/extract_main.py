from datetime import datetime

from models import Company, DataSource, ExtractStatus


extraction_types = [
    'AlphaVantage'
]

def init_data_sources():
    for extraction_type in extraction_types:
        DataSource.create(name = extraction_type)


def init_extract_statuses():
    companies = Company.select()
    for company in companies:
        missing_extract_statuses = set(extraction_types) \
            - set([es.extraction_type for es in company.extract_statuses])

        for extraction_type in missing_extract_statuses:
            ExtractStatus.create(
                company = company,
                extraction_type = extraction_type,
                extracted_until = datetime.min,
                last_successful_extraction_time = datetime.min,
                error_message = None
            )

init_data_sources()
init_extract_statuses()
