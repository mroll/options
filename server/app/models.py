from peewee import *


# db = SqliteQueueDatabase('app/options.db')
db = PostgresqlDatabase(
    'options',
    user='postgres',
    password='mysecretpassword',
    host='127.0.0.1'
)


class Company(Model):
    name = CharField()
    ticker = CharField()

    class Meta:
        database = db

uniq_company_name_idx = ModelIndex(Company, (Company.name,), unique=True)
Company.add_index(uniq_company_name_idx)


class Statistic(Model):
    company = ForeignKeyField(Company, backref='stats')
    date = DateField()
    func = CharField()
    value = FloatField()

    class Meta:
        database = db

uniq_stat_per_day_idx = ModelIndex(
    Statistic,
    (Statistic.company, Statistic.func, Statistic.date),
    unique=True
)
Statistic.add_index(uniq_stat_per_day_idx)


class Marker(Model):
    company = ForeignKeyField(Company, backref='markers')
    date = DateField()
    marker_type = CharField()

    class Meta:
        database = db

uniq_marker_per_day_idx = ModelIndex(
    Marker,
    (Marker.company, Marker.date, Marker.marker_type),
    unique=True
)
Marker.add_index(uniq_marker_per_day_idx)


class ExtractStatus(Model):
    company = ForeignKeyField(Company, backref='extract_statuses')
    extraction_type = CharField()
    extracted_until = DateTimeField()
    last_successful_extraction_time = DateTimeField()
    error_message = CharField(null = True)
    extracting_now = BooleanField(default = False)

    class Meta:
        database = db


class DataSource(Model):
    name = CharField()

    class Meta:
       database = db


class RequestLog(Model):
    data_source = ForeignKeyField(DataSource, backref='request_logs')
    request_time = DateTimeField()
    url = CharField()

    class Meta:
       database = db


request_time_idx = ModelIndex(
    RequestLog,
    (RequestLog.data_source, RequestLog.request_time)
)
RequestLog.add_index(request_time_idx)


db.connect()
db.create_tables([
    Company,
    DataSource,
    ExtractStatus,
    Marker,
    RequestLog,
    Statistic
])
