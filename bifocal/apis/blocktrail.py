import requests
from bifocal import utils, models
from coindesk import Coindesk


class Blocktrail:

    def __init__(self, key):
        self._key = key
        self._chart = Coindesk.get_chart()

    def _request(self, route, **kwargs):
        opts = '&%s' % utils.encode_args(kwargs) if kwargs else ''

        uri = ('https://api.blocktrail.com/v1/btc/%s?api_key=%s%s'
               % (route, self._key, opts))

        ret = requests.get(uri)
        return utils.parse_json(ret)

    def get_address_transactions(self, address):
        data = self._request(
            'address/%s/transactions' % address,
            limit=200
        )

        page = 1
        tx_list = [self._parse_tx(tx, address) for tx in data['data']]

        while data['total'] > data['per_page'] * page:
            page += 1

            data = self._request(
                'address/%s/transactions' % address,
                limit=200,
                page=page
            )
            tx_list += [self._parse_tx(tx, address) for tx in data['data']]

        return utils.flatten(tx_list)

    def _parse_tx(self, tx, address):
        inputs, outputs = self._clean_tx(tx)
        tx_map = utils.distribute(inputs, outputs)

        transactions = []

        fee = int(tx['total_fee'])
        stamp = utils.date_to_timestamp(tx['time'].split('+')[0],
                                        '%Y-%m-%dT%H:%M:%S')
        date = utils.timestamp_to_date(stamp, '%Y-%m-%d')

        if date in self._chart:
            price = self._chart[date]
        else:
            price = Coindesk.get_price_by_timestamp(stamp)

        for in_addr, in_value in inputs.iteritems():
            if in_addr == address:
                transactions.append(models.Transaction(
                    timestamp=stamp,
                    quantity=tx_map[in_addr]['fee'],
                    asset='BTC',
                    price=price,
                    id=tx['hash'],
                    source=in_addr,
                    destination='fee',))

            for out_addr, out_value in outputs.iteritems():
                if address not in [in_addr, out_addr]:
                    continue
                transactions.append(models.Transaction(
                    timestamp=stamp,
                    quantity=tx_map[in_addr][out_addr],
                    asset='BTC',
                    price=price,
                    id=tx['hash'],
                    source=in_addr,
                    destination=out_addr
                ))

        return transactions

    def _clean_tx(self, tx):
        input_addresses = {}
        output_addresses = {}

        inputs = tx['inputs']
        outputs = tx['outputs']

        for i in inputs:
            addr = (i['address'] if 'address' in i
                    else self._get_bare_multisig(inputs, i['index']))

            value = int(i['value'])

            if addr not in output_addresses:
                input_addresses[addr] = value
            else:
                input_addresses[addr] += value

        for o in outputs:
            if int(o['value']) == 0:
                continue

            addr = (o['address'] if 'address' in o
                    else self._get_bare_multisig(outputs, o['index']))
            value = int(o['value'])

            if addr not in output_addresses:
                output_addresses[addr] = value
            else:
                output_addresses[addr] += value

        return input_addresses, output_addresses

    def _get_bare_multisig(self, entries, index):
        for e in entries:
            if e['index'] == index:
                addresses = sorted(e['multisig_addresses'])
                multi_address = ('%s_%s_%s_%s_%s' % (e['multisig'][0],
                                                     addresses[0],
                                                     addresses[1],
                                                     addresses[2],
                                                     e['multisig'][-1]))

        return multisig_addresses
