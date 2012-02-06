import sys, os

sys.path.append(os.path.dirname(__file__) + '/..')

from tornado_crontab import CronTab
from tornado.ioloop  import IOLoop

def log():
    import time
    print "log: %0.2f" % time.time()

ct = CronTab()
ct.add_event("* * * * *", log)
IOLoop.instance().start()
