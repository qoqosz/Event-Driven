class Handler(object):
    def __init__(self, data_parser, listeners=None):
        self.data_parser = data_parser
        self.listeners = [] if listeners is None else listeners

    def notify(self, event=None):
        if event is not None:
            for listener in self.listeners:
                listener.receive(event)

    def add_listener(self, listener):
        self.listeners.append(listener)

    def run(self):
        for event in self.data_parser:
            self.notify(event)


class Event(object):
    code = '__GenericEvent__'

    def __init__(self, code, line):
        for sub in Event.__subclasses__():
            if sub.code == code:
                self.__class__ = sub
                self.set_from(line)

    def set_from(self, line):
        raise NotImplementedError('Implement set_from()')


class Listener(object):
    def receive(self, event):
        if event.code in self.codes:
            self.process(event)

    def process(self, event):
        raise NotImplementedError('Implement process()')


class Data(object):
    def __iter__(self):
        raise NotImplementedError('Implement __iter__()')


class DataParser(object):
    def __init__(self, data):
        self.data = data

    def __iter__(self):
        for line in self.data:
            yield self.parse(line)

    def parse(self, line):
        return line
