class Logger:
    def __init__(self, logfile):
        self._logfile = logfile
        self._logno = 0

    def write_startlog(self, start_message):
        with open(self._logfile, 'a') as f:
            f.write(start_message)

    def write_datalog(self, logtimestr, temp, humi, co2, tvoc):
        with open(self._logfile, 'a') as f:
            if self._logno == 0:
                f.write('%4s %14s %2s %2s %4s %3s\n' %
                        ('No.', 'Datetime', 'TC', 'H%', 'CO2', 'TVOC'))
                self._logno = 1

            f.write('%4d %14s %2d %2d %4d %3d\n' %
                    (self._logno, logtimestr, temp, humi, co2, tvoc))
            self._logno += 1

    def write_synclog(self, logtimestr, sync_mark):
        with open(self._logfile, 'a') as f:
            f.write('%4s %14s\n' % (sync_mark, logtimestr))
