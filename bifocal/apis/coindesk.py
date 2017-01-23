import requests
import json
from bifocal import utils
from datetime import datetime


class Coindesk:

    def __init__(self):
        self._chart = self._get_chart()
        self._current = self._get_price_today()

    def _get_chart(self):
        uri = ('https://api.coindesk.com/v1/bpi/historical/close.json?'
               'start=2010-07-17&end=2020-01-01')
        ret = requests.get(uri)
        return utils.parse_json(ret)['bpi']

    def _get_price_today(self):
        uri = 'https://api.coindesk.com/v1/bpi/currentprice.json'
        ret = requests.get(uri)
        return float(utils.parse_json(ret)['bpi']['USD']['rate'])

    def get_price_by_date(self, date):
        if date == datetime.today().date().strftime("%Y-%m-%d"):
            return self._get_price_today()
        return self._chart[date]

    def get_price_by_timestamp(self, timestamp):
        date = utils.timestamp_to_date(timestamp, "%Y-%m-%d")
        return self.get_price_by_date(date)
