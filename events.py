from abc import ABCMeta, abstractmethod


class Handler(object):
    """Class covering the main event loop.

    Parameters
    ----------
    parser : events.Parser
        Iterable object yielding an events.Event object.
    listeners : list
        List events.Listener that may process event from the main loop.
    """
    def __init__(self, parser, listeners=None):
        self.parser = parser
        self.listeners = [] if listeners is None else listeners

    def notify(self, event=None):
        """Notifies all listeners about new event.

        Parameters
        ----------
        event : events.Event, optional
            If provided, all subscribed listeners will be notified about event.
        """
        if event is not None:
            for listener in self.listeners:
                listener.receive(event)

    def add_listener(self, listener):
        """Subscribes a listener.

        Parameters
        ----------
        listener : events.Listener

        Returns
        -------
        self : events.Handler
            Returns self for chaining.
        """
        self.listeners.append(listener)

        return self

    def run(self):
        """Runs the main events loop.
        """
        for event in self.parser:
            self.notify(event)


class Event(object):
    """Defines a generic event. Event is transformed to a specific subclass
    instance based on a code provided.

    Parameters
    ----------
    code : string
        Event's code for subclass transformation.
    line : raw data
        Raw data from the underlying events.Data object.
    """

    code = '__GenericEvent__'

    def __init__(self, code, line):
        for sub in Event.__subclasses__():
            if sub.code == code:
                self.__class__ = sub
                self.from_line(line)

    def from_line(self, line):
        """Converts raw data input into Event object.
        Each subclass should implement this method.

        Parameters
        ----------
        line : raw data
            Raw data."""
        raise NotImplementedError('Implement from_line()')


class Listener(object):
    """Abstract Base Class (ABC) for classes that will handle events
    processing."""
    __metaclass__ = ABCMeta

    codes = ('__GenericEvent__', )

    def receive(self, event):
        if event.code in self.codes:
            self.process(event)

    @abstractmethod
    def process(self, event):
        """Processes received event. To be implemented in each subclass."""
        raise NotImplementedError('Implement process()')


class Data(object):
    """Abstract class for data handling. There is only one requirement imposed
    on a Data object - it has to be iterable."""
    __metaclass__ = ABCMeta

    @abstractmethod
    def __iter__(self):
        raise NotImplementedError('Implement __iter__()')


class Parser(object):
    """Parser takes data as an input, processes each line in a stream and
    yields event by event.

    Parameters
    ----------
    data : events.Data
        Data object.
    """
    __metaclass__ = ABCMeta

    def __init__(self, data):
        self.data = data

    def __iter__(self):
        for line in self.data:
            yield self.parse(line)

    @abstractmethod
    def parse(self, line):
        """Converts line to a coresponding events. To be implemented in a
        subclass.

        Parameters
        ----------
        line : raw data
        """
        raise NotImplementedError('Implement parse()')
