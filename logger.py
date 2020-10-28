class Logger:
    def __init__(self, logfile):
        self._logfile = logfile

    def write_startlog(self, start_message):
        with open(self._logfile, 'a') as f:
            f.write(start_message)

    def write_datalog(self, logno, logtimestr, temp, humi, co2, tvoc):
        with open(self._logfile, 'a') as f:
            if logno == 1:
                f.write('%4s %14s %2s %2s %4s %3s\n' %
                        ('No.', 'Datetime', 'TC', 'H%', 'CO2', 'TVOC'))
            f.write('%4d %14s %2d %2d %4d %3d\n' %
                    (logno, logtimestr, temp, humi, co2, tvoc))

    def write_synclog(self, logtimestr, sync):
        if sync > 0:
            mark = '*'
        elif sync == -1:
            mark = 'x'
        elif sync == -2:
            mark = '-'
        else:
            mark = ' '
        with open(self._logfile, 'a') as f:
            f.write('%4s %14s\n' % (mark, logtimestr))
