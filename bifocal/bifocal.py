import models
import apis
import accounting
import utils


class Bifocal():

    def __init__(self, addresses=[], assets=[],
                 polo_key=None, polo_secret=None):

        self._polo = apis.Polo(polo_key, polo_secret)
        self._blockscan = apis.Blockscan()
        self._coindesk = apis.Coindesk()
        self._blockchain = apis.Blockchain()

        self._assets = assets
        self._transactions = {}

        self._addresses = addresses
        self._add_exchange_addresses()

        self.wallet = models.Wallet(self._addresses)

        self.make_transaction_lists()

    def _add_exchange_addresses(self):
        self._add_polo_addresses()

    def _add_polo_addresses(self):
        for asset in self._assets:
            self._add_addresses(polo.get_deposit_addresses_by_asset(asset))

    def _add_addresses(self, addresses):
        self._addresses += set(addresses) - set(self._addresses)

    def _add_exchange_sales(self):
        pass

    def make_transaction_lists(self):
        for asset in self._assets:
            self._transactions[asset] = utils.flatten(map(
                lambda a: self._blockscan.get_address_transactions(a, asset),
                self.wallet
            ))
        self._transactions[asset] = utils.flatten(map(
            lambda a: self._blockchain.get_address_transactions(a)
        ))
        self._add_exchange_sales()
        self._add_prices()

    def _add_prices(self):
        for asset in assets:
            pass
