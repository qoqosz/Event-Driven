import pandas_datareader as pdr
from events import Event, Data, Parser, Handler, Listener


class Quote(Event):
    code = 'quote'

    def __init__(self, date, open, high, low, close, volume):
        self.date = date
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume


class StockData(Data):
    def __init__(self, sym):
        self.sym = sym
        self.data = pdr.get_data_google(sym)

    def __iter__(self):
        for index, row in self.data.iterrows():
            yield (index, row)


class StockParser(Parser):
    def parse(self, line):
        index, row = line
        return Quote(index.date(), *row)


class StrategyMovingAverage(Listener):
    codes = ('quote', )

    def __init__(self, n):
        super().__init__()
        self.n = n
        self.prices = []

    def add(self, px):
        if len(self.prices) == self.n:
            self.prices = self.prices[1:]
        self.prices.append(px)

    @property
    def avg(self):
        if self.prices:
            return sum(self.prices) / len(self.prices)
        return 0.0

    def process(self, event):
        self.add(event.open)


if __name__ == '__main__':
    # TODO: How to make parent class auto init subclasses?
    data = StockData('AAPL')
    n = 10
    parser = StockParser(data)
    ma = StrategyMovingAverage(n)

    print('Starting!')

    handler = Handler(parser)
    handler.add_listener(ma)
    handler.run()

    print(f'Moving average from the latest {n} days: {ma.avg}')
