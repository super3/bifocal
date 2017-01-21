import requests
import json
import utils


class Coindesk:

    def __init__(self):
        pass

    def _request(self, command, **kwargs):
        uri = ('https://min-api.cryptocompare.com/data/%s?%s'
               % (command % utils.encode_args(kwargs)))
        ret = requests.get(uri)
        return utils.parse_json(ret)
