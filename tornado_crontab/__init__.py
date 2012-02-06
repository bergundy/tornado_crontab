import tornado.ioloop
from datetime import datetime
import time

from event import Event

class CronTab(object):
    def __init__(self, io_loop = None, run = True):
        self.events   = dict()
        self.io_loop  = io_loop or tornado.ioloop.IOLoop.instance()
        self.currid   = -1
        if run:
            self.run()

    def next_event_id(self):
        self.currid += 1
        return self.currid

    def add_event(self, *args, **kwargs):
        event = Event(self.next_event_id(), *args, **kwargs)
        self.events[event.id] = event
        return event.id

    def del_event(self, id):
        if id in self.events:
            del self.events[id]

    def get_event(self, id):
        return self.events.get(id)

    def check_cron(self):
        t = datetime(*datetime.now().timetuple()[:5])

        for e in self.events.itervalues():
            if e.check(t):
                e.action(*e.args, **e.kwargs)

        self.run()

    def run(self):
        next_runtime = time.time() + 60
        next_runtime = next_runtime - next_runtime % 60
        self.io_loop.add_timeout(next_runtime, self.check_cron)
