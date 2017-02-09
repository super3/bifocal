import csv
from bifocal import utils, models
from bifocal.apis import Blockchain


# Notes:
# The TXIDs must be added to the CSV by hand.

class Celery(object):

    @staticmethod
    def get_transfer_txids(file_path):
        data = Celery._get_data(file_path)
        txids = []
        for tx in data:
            if len(tx['TXID']) == 64:
                txids.append(tx['TXID'])
        return txids

    @staticmethod
    def get_transactions(file_path):
        data = Celery._get_data(file_path)
        txns = []
        for tx in data:
            dollars = Celery._parse_dollars(tx)
            stamp = utils.date_to_timestamp(tx['Date'], '%b %d %Y')
            price = round(dollars / float(tx['Amount']), 2)
            tx['Amount'] = int(round(float(tx['Amount']) * 100000000))

            if tx['Type'] == 'Buy':
                txns.append(models.Transaction(
                    timestamp=stamp,
                    quantity=tx['Amount'],
                    price=price,
                    asset='BTC',
                    id=tx['TXID'],
                    source='Celery',
                    destination='Celery'))

            elif tx['Type'] == 'Sell':
                txns.append(models.Transaction(
                    timestamp=stamp,
                    quantity=tx['Amount'],
                    price=price,
                    asset='BTC',
                    id=tx['TXID'],
                    source='Celery',
                    destination='Celery'))

        return txns

    @staticmethod
    def _get_data(file_path):
        with open(file_path, 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            return [row for row in reader]

    @staticmethod
    def _parse_dollars(tx):
        dollars = tx['Dollars']
        if dollars[0] == '(':
            dollars = dollars.lstrip('($').rstrip(')').replace(',', '')
        elif dollars[0] == '$':
            dollars = dollars.lstrip('$').replace(',', '')
        return float(dollars)
