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
    def get_tx_by_id(txid):
        data = Blockchain._request('rawtx', txid)
        return data

    @staticmethod
    def get_address_transactions(address):
        data = Blockchain._request('rawaddr', address)
        transactions = data['txs']
        tx_list = utils.flatten(
            [Blockchain._parse_tx(tx, address) for tx in transactions])

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
    def _parse_tx(tx, address):
        inputs, outputs = Blockchain._clean_tx(tx)

        transactions = []

        tx_map = utils.distribute(inputs, outputs)

        chart = Coindesk.get_chart()
        stamp = int(tx['time'])
        date = utils.timestamp_to_date(stamp, '%Y-%m-%d')

        if date in chart:
            price = chart[date]
        else:
            price = Coindesk.get_price_by_timestamp(stamp)

        for input_addr in inputs:
            transactions.append(models.Transaction(
                timestamp=stamp,
                quantity=tx_map[input_addr]['fee'],
                asset='BTC',
                price=price,
                id=tx['hash'],
                source=input_addr,
                destination='fee',))

            for output_addr in outputs:
                if address not in [input_addr, output_addr]:
                    continue
                transactions.append(models.Transaction(
                    timestamp=stamp,
                    quantity=tx_map[input_addr][output_addr],
                    asset='BTC',
                    price=price,
                    id=tx['hash'],
                    source=input_addr,
                    destination=output_addr))

        return transactions

    @staticmethod
    def _clean_tx(tx):
        input_addresses = {}
        output_addresses = {}

        inputs = [i['prev_out'] for i in tx['inputs']]
        outputs = tx['out']

        for i in inputs:
            addr = (i['addr'] if 'addr' in i
                    else Blockchain._get_bare_multisig(tx))

            value = int(i['value'])

            if addr not in input_addresses:
                input_addresses[addr] = value
            else:
                input_addresses[addr] += value

        for o in outputs:
            if int(o['value']) == 0:
                continue

            addr = (o['addr'] if 'addr' in o
                    else Blockchain._get_bare_multisig(tx))
            value = int(o['value'])

            if addr not in output_addresses:
                output_addresses[addr] = value
            else:
                output_addresses[addr] += value

        return input_addresses, output_addresses

    @staticmethod
    def _get_bare_multisig(tx):
        raise NotImplementedError
