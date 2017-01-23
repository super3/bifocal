import requests
from bifocal import utils, models
from coindesk import Coindesk


class Blockchain:

    def __init__(self):
        self._coindesk = Coindesk()

    def _request(self, command, arg):
        uri = 'https://blockchain.info/%s/%s' % (command, arg)
        ret = requests.get(uri)
        return utils.parse_json(ret)

    def get_address_transactions(self, address):
        data = self._request('rawaddr', address)
        transactions = data['txs']
        tx_list = utils.flatten(map(self._parse_tx, transactions))

        for tx in tx_list:
            if tx.data['source'] == address:
                tx.invert_quantity()

        tx_list = filter(
            (lambda k: k.data['source'] == address
             or k.data['destination'] == address),
            tx_list
        )

        return tx_list

    def _parse_tx(self, tx):
        inputs = tx['inputs']
        outputs = tx['out']

        total_inputs = sum([i['prev_out']['value'] for i in inputs])
        total_outputs = sum([i['value'] for i in outputs])
        fee = total_inputs - total_outputs

        input_addresses = self._clean_inputs(inputs)
        output_addresses = self._clean_outputs(outputs)

        transactions = []

        for input_addr, in_value in input_addresses.iteritems():
            proportion = float(in_value) / total_inputs

            for output_addr, out_value in output_addresses.iteritems():
                stamp = int(tx['time'])
                quantity = round(out_value * proportion) / 100000000.0
                t = models.Transaction(
                    timestamp=stamp,
                    quantity=quantity,
                    asset='BTC',
                    price=self._coindesk.get_price_by_timestamp(stamp),
                    id=tx['hash'],
                    source=input_addr,
                    destination=output_addr,
                    fee=proportion * fee
                )
                transactions.append(t)

        return transactions

    def _clean_inputs(self, inputs):
        input_addresses = {}
        for i in inputs:
            addr = i['prev_out']['addr']
            value = int(i['prev_out']['value'])
            if addr not in input_addresses:
                input_addresses[addr] = value
            else:
                input_addresses[addr] += value
        return input_addresses

    def _clean_outputs(self, outputs):
        output_addresses = {}
        for o in outputs:
            if 'addr' not in o or int(o['value']) == 0:
                continue
            addr = o['addr']
            value = int(o['value'])
            if addr not in output_addresses:
                output_addresses[addr] = value
            else:
                output_addresses[addr] += value
        return output_addresses
