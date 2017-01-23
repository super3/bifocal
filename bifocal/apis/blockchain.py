import requests
from bifocal import utils, models


class Blockchain:

    def __init__(self):
        pass

    def _request(self, command, arg):
        uri = 'https://blockchain.info/%s/%s' % (command, arg)
        ret = requests.get(uri)
        return utils.parse_json(ret)

    def get_address_transactions(self, address):
        data = self._request('rawaddr', address)
        transactions = data['txs']
        return flatten(map(self._parse_tx, transactions))

    def _parse_tx(self, tx):
        inputs = tx['inputs']
        outputs = tx['out']

        total_inputs = sum([i['prev_out']['value'] for i in inputs])
        total_outputs = sum([i['value'] for i in outputs])

        transactions = []

        for i in inputs:
            i['proportion'] = round(
                float(i['prev_out']['value']) / total_inputs
            )
            for o in outputs:
                t = models.Transaction(
                    timestamp=tx['time'],
                    quantity=round(o['value'] * i['proportion']),
                    asset='BTC',
                    id=tx['hash'],
                    source=i['addr'],
                    destination=o['addr']
                )
                transactions.append(t)

        return transactions
