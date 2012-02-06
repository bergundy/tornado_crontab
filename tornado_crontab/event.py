import re
from datetime import datetime, timedelta

class Event(object):
    class Universe(set):
        def __contains__(self, item): return True

    _universe = Universe()

    def __init__(self, id, timing, action, args=(), kwargs={}):
        m = re.match("^(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)$", timing)
        if not m:
            raise TypeError("'timing' argument pattern mismatch")

        self.mins   = self._get_set(m.group(1), 60)
        self.hours  = self._get_set(m.group(2), 24)
        self.days   = self._get_set(m.group(3), 31)
        self.months = self._get_set(m.group(4), 12)
        self.dow    = self._get_set(m.group(5), 7)

        self.id     = id
        self.action = action
        self.args   = args
        self.kwargs = kwargs

    def _get_set(self, pattern, units):
        pattern = pattern.split(",")
        ret     = set()

        for p in pattern:
            if p == "*":
                return self._universe
            elif re.match("^\d+$", p):
                ret.add(int(p))
            else:
                m = re.match("^\*/(\d+)$", p)
                if m:
                    repeat = int(m.group(1))
                    ret   |= set([x*repeat for x in range(units/repeat)])
                else:
                    m = re.match("^(\d+)-(\d+)$", p)
                    if m:
                        ret |= set(range(int(m.group(1)), int(m.group(2))+1))
                    else:
                        raise TypeError("invalid pattern %s" %(p))

        return ret

    def check(self, t):
        return ((t.minute     in self.mins)   and
                (t.hour       in self.hours)  and
                (t.day        in self.days)   and
                (t.month      in self.months) and
                (t.weekday()  in self.dow))

    def next_runtime(self):
        n = datetime(*datetime.now().timetuple()[:5]) + timedelta(minutes = 1)

        while True:
            if n.month not in self.months:
                n = n.replace(year = n.year + (n.month+1) / 12, month = (n.month+1) % 12, day = 1, hour = 0, minute = 0)
                continue
            if n.day not in self.days \
            or n.weekday() not in self.dow:
                n += timedelta(days = 1)
                n = n.replace(hour = 0, minute = 0)
                continue
            if n.hour not in self.hours:
                n += timedelta(hours = 1)
                n = n.replace(minute = 0)
                continue
            if n.minute not in self.mins:
                n += timedelta(minutes = 1)
                continue

            return n

if __name__ == '__main__':
    e = Event("---", "2,3-5,*/5 19 * 9-12 0", str)
    mins = list(e.mins)
    print e.next_runtime()
    mins.sort()
    print mins
