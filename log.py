from events import Handler, Event, Listener, Data, DataParser

# Dynamically check what events should be created - yield


class LogData(Data):
    def __init__(self, log):
        self.log = log

    def __iter__(self):
        with open(self.log) as f:
            for line in f:
                yield line


class LogParser(DataParser):
    def get_code (self, line):
        spaces = [i for i, char in enumerate(line)
                  if char == ' ']
        start, end = spaces[1:3]

        return line[start+1:end]

    def parse(self, line):
        code = self.get_code(line)
        return Event(code, line)


class Event1and2Listener(Listener):
    codes = ['Event1', 'Event2']

    def process(self, event):
        print(f'Caught {event.code} with value {event.value}')


class Event1Listerner(Listener):
    codes = ['Event1']

    def process(self, event):
        print(f'Caught {event.code} by Event1Listerner')


class Event2Listerner(Listener):
    codes = ['Event2']

    def process(self, event):
        print(f'Caught {event.code} by Event2Listerner')


class Event1(Event):
    code = 'Event1'

    def __init__(self, a, b):
        self.a, self.b = a, b

    def set_from(self, line):
        self.a, self.b = 0.1, 0.2

    @property
    def value(self):
        return f'a={self.a}, b={self.b}'


class Event2(Event):
    code = 'Event2'

    def __init__(self, sit, abc):
        self.sit, self.abc = sit, abc

    def set_from(self, line):
        self.sit, self.abc = 'sit', 'abc'

    @property
    def value(self):
        return f'sit={self.sit}, abc={self.abc}'


if __name__ == '__main__':
    log = LogData('data.txt')
    parser = LogParser(log)

    events_listener = Event1and2Listener()
    ev1_l = Event1Listerner()
    ev2_l = Event2Listerner()

    handler = Handler(parser)
    handler.add_listener(events_listener)
    handler.add_listener(ev1_l)
    handler.add_listener(ev2_l)
    handler.run()
