import requests
import json
from ifo import utils


class Coindesk:

    def __init__(self):
        self._ret = self._request(
            start='2010-07-17',
            end='2020-01-01'
        )
        self._chart = self._ret['bpi']

    def _request(self, **kwargs):
        uri = ('http(s)://api.coindesk.com/v1/bpi/historical/close.json?'
               % utils.encode_args(kwargs))
        ret = requests.get(uri)
        return utils.parse_json(ret)

    def get_price_by_date(self, date):
        return self._chart[date]

    def get_price_by_timestamp(self, timestamp):
        date = utils.timestamp_to_date(timestamp, "%Y-%m-%d")
        return self.get_price_by_date(date)
