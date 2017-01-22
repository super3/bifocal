class Wallet:
    def __init__(self, addresses):
        self._addresses = addresses
        self._current = 0

    def __iter__(self):
        return self

    def next(self):
        self._current += 1
        if self._current > len(self._addresses):
            self._current = 0
            raise StopIteration
        return self._addresses[self._current - 1]

    
