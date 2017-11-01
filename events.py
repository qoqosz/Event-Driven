from abc import ABC, abstractmethod
from collections import deque
import logging


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
        self.log = logging.getLogger(self.__class__.__name__)
        self.parser = parser
        self.queue = deque()
        self.listeners = []
        if listeners is not None:
            for listener in listeners:
                self = self.add_listener(listener)
        self.log.debug('Handler created.')

    def notify(self, event=None):
        """Notifies all listeners about new event.

        Parameters
        ----------
        event : events.Event, optional
            If provided, all subscribed listeners will be notified about event.
        """
        self.log.debug('Running notify loop.')
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
        listener.handler = self
        self.listeners.append(listener)
        self.log.debug('Added listener.')

        return self

    def enqueue(self, event):
        """Adds event to the queue."""
        self.queue.append(event)
        self.log.debug('Added event to queue: %r', event)

    def run(self):
        """Runs the main events loop."""
        for event in self.parser:
            if not event:
                continue
            self.enqueue(event)

            while self.queue:
                e = self.queue.popleft()
                self.log.debug('Notifying listeners about event: %r, '
                               'queue len: %d.',
                               e, 1+len(self.queue))
                self.notify(e)
                self.log.debug('Done with notifying.')


class Event(ABC):
    """Defines a generic event. Specific events should be directly inherited
    from this class."""
    code = '__GenericEvent__'

    def __repr__(self):
        return self.code + ' ' + str(self.value)

    def from_line(self, line):
        raise NotImplementedError('Implement from_line()')


class Listener(ABC):
    """Abstract Base Class (ABC) for classes that will handle events
    processing."""
    codes = tuple()

    def __init__(self):
        self.handler = None
        self.log = logging.getLogger(self.__class__.__name__)

    def receive(self, event):
        if event.code in self.codes:
            self.process(event)

    def emit(self, event):
        self.handler.enqueue(event)
        self.log.debug('Emitted event: %r', event)

    @abstractmethod
    def process(self, event):
        raise NotImplementedError('Implement process()')


class Data(ABC):
    @abstractmethod
    def __iter__(self):
        raise NotImplementedError('Implement __iter__()')


class Parser(ABC):
    def __init__(self, data):
        self.data = data

    def __iter__(self):
        for line in self.data:
            yield self.parse(line)

    @abstractmethod
    def parse(self, line):
        raise NotImplementedError('Implement parse()')
