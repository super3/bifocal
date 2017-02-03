import requests
from bifocal import utils
from datetime import date


class Coindesk(object):

    @staticmethod
    def get_chart():
        uri = ('https://api.coindesk.com/v1/bpi/historical/close.json?'
               'start=2010-07-17&end=2020-01-01')
        ret = requests.get(uri)
        return utils.parse_json(ret)['bpi']

    @staticmethod
    def _get_date(date):
        uri = ('https://api.coindesk.com/v1/bpi/historical/close.json?'
               'start=%s&end=%s') % (date, date)
        ret = requests.get(uri)
        return float(utils.parse_json(ret)['bpi'][date])

    @staticmethod
    def _get_price_today():
        uri = 'https://api.coindesk.com/v1/bpi/currentprice.json'
        ret = requests.get(uri)
        return float(utils.parse_json(ret)['bpi']['USD']['rate'])

    @staticmethod
    def get_price_by_date(date_string):
        if date_string == date.today().strftime("%Y-%m-%d"):
            return Coindesk._get_price_today()
        return Coindesk._get_date(date_string)

    @staticmethod
    def get_price_by_timestamp(timestamp):
        date = utils.timestamp_to_date(timestamp, "%Y-%m-%d")
        return Coindesk.get_price_by_date(date)
