from events import Handler, Event, Listener
from logevents import LogData, LogParser
import logging
import re
#import ipdb


def find_float(var, line, sep='='):
    m = re.search(var + sep + '(\d+\.*\d*)', line)
    if m:
        return float(m.group(1))
    raise ValueError('Cannot match ' + var)

def find_string(var, line, sep='=', within='"'):
    m = re.search(var + sep + within + '(\w+)' + within, line)
    if m:
        return m.group(1)
    raise ValueError('Cannot match ' + var)


class Event1(Event):
    code = 'Event1'

    def from_line(self, line):
        self.a, self.b = find_float('a', line), find_float('b', line)

    @property
    def value(self):
        return f'a={self.a}, b={self.b}'


class Event2(Event):
    code = 'Event2'

    def from_line(self, line):
        self.sit, self.abc = find_float('sit', line), find_string('abc', line)

    @property
    def value(self):
         return f'sit={self.sit}, abc={self.abc}'


class ListenerEvent(Event):
    code = 'Event3'

    def __init__(self, value):
        self.value = value


class Event1and2Listener(Listener):
    codes = ('Event1', 'Event2')

    def process(self, event):
        print(f'Caught {event.code} with value {event.value} by '
              'Event1and2Listener')
        #ipdb.set_trace()
        e1, e2 = (ListenerEvent(value='event emitted by listener'),
                  ListenerEvent(value='another event emitted by listener'))
        print(f'Code check: {e1.code}, {e2.code}')
        self.emit(e1)
        self.emit(e2)
        print('Signals emitted')


class Event1Listener(Listener):
    codes = ('Event1', )

    def process(self, event):
        print(f'Caught {event.code} by Event1Listerner')


class Event2Listener(Listener):
    codes = ('Event2', )

    def process(self, event):
        print(f'Caught {event.code} by Event2Listerner')


class Event3Listener(Listener):
    codes = ('Event3', )

    def process(self, event):
        print(f'Caught {event.code} created by other listener')


if __name__ == '__main__':
    logger = logging.getLogger()
    FORMAT = "[%(filename)s:%(lineno)s - %(name)s %(funcName)s()] %(message)s"
    logging.basicConfig(format=FORMAT)
    logger.setLevel(logging.INFO)


    log = LogData('data.txt')
    parser = LogParser(log)

    handler = Handler(parser)
    handler.add_listener(Event1and2Listener()) \
           .add_listener(Event1Listener()) \
           .add_listener(Event2Listener()) \
           .add_listener(Event3Listener())
    handler.run()
