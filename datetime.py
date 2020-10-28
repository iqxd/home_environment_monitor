import machine
import time
import network
import ntptime

ntptime.NTP_DELTA = 3155644800
ntptime.host = 'ntp1.aliyun.com'

weekdays = {
    1: 'Mon',
    2: 'Tus',
    3: 'Wen',
    4: 'Thu',
    5: 'Fri',
    6: 'Sat',
    7: 'Sun'
}

months = {
    1: 'Jan',
    2: 'Feb',
    3: 'Mar',
    4: 'Apr',
    5: 'May',
    6: 'Jun',
    7: 'Jul',
    8: 'Aug',
    9: 'Sep',
    10: 'Oct',
    11: 'Nov',
    12: 'Dec'
}


class DateTime:
    def __init__(self, wl):
        self._wl = wl
        self._rtc = machine.RTC()

    def sync(self):
        if not self._wl.isconnected():
            if not self._wl.connect():
                return -1
        try:
            ntptime.settime()
            self._rtc = machine.RTC()
        except:
            return -2
        else:
            return 1

    def get(self):
        year, month, day, weekday, hour, minute, second, _ = self._rtc.datetime(
        )
        weekday += 1
        return year, month, day, weekday, hour, minute, second

    def get_formatted(self, show_week=True, show_secs=False):
        year, month, day, weekday, hour, minute, second = self.get()
        if show_week:
            fdate = "%s %02d-%s-%d" % (weekdays[weekday], day, months[month],
                                       year)
        else:
            fdate = "%02d-%s-%d" % (day, months[month], year)
        if show_secs:
            ftime = "%02d:%02d:%02d" % (hour, minute, second)
        else:
            ftime = "%02d:%02d" % (hour, minute)
        raw = '%04d%02d%02d%02d%02d%02d' % (year, month, day, hour, minute,
                                            second)
        return fdate, ftime, raw
