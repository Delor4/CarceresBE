import math

price_by_days = {
    365: 1800,
    182: 1000,
    28: (22 * 9),
    7: (6 * 9),
    1: 9,
}


def _calc_price(days):
    for _time in price_by_days:
        if days >= _time:
            return math.ceil(days / _time) * price_by_days[_time]
    return price_by_days[1]


def calc_price(start_date, end_date):
    diff = end_date - start_date
    return _calc_price(diff.days) * 100


def calc_tax():
    return 23
