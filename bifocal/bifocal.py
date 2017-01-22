import models
import apis
import accounting


class Bifocal():

    def __init__(self, addresses=[], assets=[],
                 polo_key=None, polo_secret=None):

        self._polo = accounting.Polo(polo_key, polo_secret)
        self._blockscan = accounting.Blockscan()
        self._coindesk = accounting.Coindesk()

        self._assets = assets
        self._transactions = {}

        self._addresses = addresses
        self._add_exchange_addresses()

        self.wallet = models.Wallet(self._addresses)

        pass

    def _add_exchange_addresses(self):
        self._add_polo_addresses()

    def _add_polo_addresses(self):
        for asset in self._assets:
            self._add_addresses(polo.get_deposit_addresses_by_asset(asset))

    def _add_addresses(self, addresses):
        self._addresses += set(addresses) - set(self._addresses)
