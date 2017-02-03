import requests
from bifocal import utils, models
from coindesk import Coindesk
from blockscan import Blockscan


class Blockchain(object):

    @staticmethod
    def _request(command, arg):
        uri = 'https://blockchain.info/%s/%s' % (command, arg)
        ret = requests.get(uri)
        return utils.parse_json(ret)

    @staticmethod
    def get_address_transactions(address):
        data = Blockchain._request('rawaddr', address)
        transactions = data['txs']
        tx_list = utils.flatten(map(Blockchain._parse_tx, transactions))

        for tx in tx_list:
            if tx.data['source'] == address:
                tx.invert_quantity()

        tx_list = filter(
            (lambda k: k.data['source'] == address
             or k.data['destination'] == address),
            tx_list
        )

        return tx_list

    @staticmethod
    def _parse_tx(tx):
        total_inputs = sum([i['prev_out']['value'] for i in inputs])
        total_outputs = sum([i['value'] for i in outputs])
        fee = total_inputs - total_outputs

        input_addresses, output_addresses = Blockchain._clean_inputs(tx)

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
                    price=Coindesk.get_price_by_timestamp(stamp),
                    id=tx['hash'],
                    source=input_addr,
                    destination=output_addr,
                    fee=proportion * fee
                )
                transactions.append(t)

        return transactions

    @staticmethod
    def _clean_tx(tx):
        inputs = [tx['inputs'][i]['prev_out'] for i in tx['inputs']]
        outputs = tx['out']

        output_addresses = {}
        input_addresses = {}

        for i in inputs:
            addr = (i['addr'] if 'addr' in i
                    else Blockchain._get_bare_multisig(tx))

            value = int(i['value'])

            if addr not in input_addresses:
                input_addresses[addr] = value
            else:
                input_addresses[addr] += value

        for o in outputs:
            if o['value'] == 0:
                continue
            addr = (o['addr'] if addr in o
                    else Blockchain._get_bare_multisig(tx))

            value = int(o['value'])

            if addr not in output_addresses:
                output_addresses[addr] = value
            else:
                output_addresses[addr] += value

        return input_addresses, output_addresses

    @staticmethod
    def _get_bare_multisig(tx):
        tx = Blockscan.get_tx_by_id(tx['hash'])
        raise NotImplementedError
