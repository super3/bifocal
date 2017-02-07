import csv
from bifocal import utils, models
from bifocal.apis import Coindesk, Blockchain


class Coinbase(object):

    @staticmethod
    def get_transfer_addresses(file_path):
        data = Coinbase._get_data(file_path)
        addresses = []
        for tx in data:
            if tx['To'] != '' and (tx['To'][0] == '1' or tx['To'][0] == '3'):
                addresses.append(tx['To'])
        return addresses

    @staticmethod
    def get_transfer_txids(file_path):
        data = Coinbase._get_data(file_path)
        txids = []
        for tx in data:
            if tx['Bitcoin Hash'] != '':
                txids.append(tx['Bitcoin Hash'])
        return txids

    @staticmethod
    def get_transactions(file_path):
        data = Coinbase._get_data(file_path)
        txns = utils.flatten(map(Coinbase._parse_tx, data))
        Coinbase._add_prices(txns)
        return txns

    @staticmethod
    def _add_prices(txns):
        chart = Coindesk.get_chart()
        for tx in txns:
            if tx.price == 0.0 and tx.data['datestring'][:10] in chart:
                tx.price = chart[tx.data['datestring'][:10]]
            elif tx.price == 0.0:
                tx.price = Coindesk.get_price_by_timestamp(tx.timestamp)

    @staticmethod
    def _get_data(file_path):
        with open(file_path, 'rb') as csvfile:
            # Skip pre-header rows
            next(csvfile, None)
            next(csvfile, None)
            next(csvfile, None)
            next(csvfile, None)

            # Come on Coinbase, this was a really bad idea for a column name
            hash_msg = ('Bitcoin Hash (visit https://www.coinbase.com'
                        '/tx/[HASH] in your browser for more info)')

            reader = csv.DictReader(csvfile)
            data = [row for row in reader]
            for row in data:
                row['Bitcoin Hash'] = row[hash_msg]
            return data

    @staticmethod
    def _parse_tx(tx):
        # Making all returns lists so we can use flatten.
        stamp = Coinbase._parse_time(tx)
        quantity = int(round(float(tx['Amount']) * 100000000))

        # Coinbase Signup Gift
        if '@' in tx['To']:
            return [models.Transaction(
                        timestamp=stamp,
                        quantity=quantity,
                        asset='BTC',
                        id=tx['Notes'],
                        source='Coinbase',
                        destination='Coinbase',
                        datestring=tx['Timestamp'])]

        # Buy or Sell on Coinbase with USD
        if tx['Transfer Total'] != '':
            price = float(tx['Transfer Total']) / float(tx['Amount'])
            return [models.Transaction(
                        timestamp=stamp,
                        quantity=quantity,
                        asset='BTC',
                        price=price,
                        id=tx['To'],
                        source='Coinbase',
                        destination='Coinbase',
                        datestring=tx['Timestamp'])]

        # Transfer out of Coinbase
        if tx['To'] != '':
            return [models.Transaction(
                        timestamp=stamp,
                        quantity=quantity,
                        asset='BTC',
                        id=tx['Bitcoin Hash'],
                        source='Coinbase',
                        destination=tx['To'],
                        datestring=tx['Timestamp'])]

        # Transfer in to Coinbase
        # This is more complicated because it can have multiple inputs
        # Therefore we need to parse the TX using a block explorer
        # This is going to be a bit hacky.
        raw_tx = Blockchain._request('rawtx', tx['Bitcoin Hash'])

        for o in raw_tx['out']:
            if int(o['value']) == abs(quantity):
                address = o['addr']

        txns = Blockchain._parse_tx(raw_tx, address)

        for tx in txns:
            tx.data['destination'] = 'Coinbase'

        return txns

    @staticmethod
    def _parse_time(tx):
        """
        Terrible Timezone Parsing
        """
        form_string = '%Y-%m-%d %H:%M:%S'
        return (utils.date_to_timestamp(tx['Timestamp'][:19], form_string)
                - int(tx['Timestamp'][20:23]) * 60 * 60
                - int(tx['Timestamp'][23:]) * 60)
