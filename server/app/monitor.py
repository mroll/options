from datetime import date, timedelta

from models import Company, Marker, Statistic


def daterange(start_date, end_date):
    for i in range(int((end_date - start_date).days)):
        yield start_date + timedelta(i)


# Compute the first derivative by backward difference
def slopes(xs):
    return [xs[i+1] - xs[i] for i in range(len(xs)-1)]


def macd_pulling_up(company, start_date, end_date):
    macd_over_daterange = [macd.value for macd in company.stats.where(
        Statistic.date >= start_date,
        Statistic.date < end_date,
        Statistic.func == 'macd_hist'
    )]

    macd_slopes = slopes(macd_over_daterange)

    # if the week didn't start sloping down,
    # macd was not pulling up
    if macd_slopes[0] > 0:
        return False

    # make sure macd slope is monotonically increasing across
    # the date range
    for i in range(len(macd_slopes)-1):
        if macd_slopes[i] > macd_slopes[i+1]:
            return False

    return True


def mark(company, date, marker_type):
    Marker.create(company = company, date = date, marker_type = marker_type)


def mark_put_selling_opportunities(company, start_date, end_date):
    for date in daterange(start_date + timedelta(8), end_date):
        try:
            rsi, = company.stats.where(Statistic.date == date, Statistic.func == 'rsi')

            oversold = rsi.value < 40

            if oversold and macd_pulling_up(company, date - timedelta(7), date):
                print('put_selling_opportunity', date)
                mark(company, date, 'put_selling_opportunity')

            # for days w/ no data (weekends, holidays)
        except ValueError:
            continue


companies = Company.select()
start_date = date(2020, 6, 1)
end_date = date(2020, 10, 1)

for company in companies:
    print("processing {} ({})".format(company.name, company.ticker))
    mark_put_selling_opportunities(company, start_date, end_date)
    print()
