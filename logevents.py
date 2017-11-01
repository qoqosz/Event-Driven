from events import Event, Data, Parser


def event_factory(code, line):
    for sub in Event.__subclasses__():
        if sub.code == code:
            event = sub.__new__(sub)
            # event.__class__ = sub
            event.from_line(line)

            return event
    return None


class LogData(Data):
    def __init__(self, log):
        self.log = log

    def __iter__(self):
        with open(self.log) as f:
            for line in f:
                yield line


class LogParser(Parser):
    def get_code(self, line):
        spaces = [i for i, char in enumerate(line)
                  if char == ' ']
        start, end = spaces[1:3]

        return line[start+1:end]

    def parse(self, line):
        code = self.get_code(line)
        event = event_factory(code, line)

        return event
