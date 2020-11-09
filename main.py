from machine import Pin, Timer
import time
from wireless import Wireless
from datetime import DateTime
from display import Display
from sensors import TempHumi,CO2TVOC
from logger import Logger

# constants
W = 128
H = 64
B = 2
WIFI_NAME = 'wifiname'
WIFI_PASSWORD = 'wifipassword'
DURATION_SECS = 2
SYNC_DURATION_COUNT = 900 // DURATION_SECS  # measure per secs
LOG_DURATION_COUNT = 240 // DURATION_SECS  # measure per secs
LOG_FILENAME = 'timelog.txt'

# hardware GPIO Pins
# D1 Mini Board
DC = 2  # D4
RES = 0  # D3
CS = 15  # D8
DHT = 12  # D6
SCL = 5  # D1
SDA = 4  # D2


class Station:
    def __init__(self):
        self.disp = Display(Pin(DC), Pin(RES), Pin(CS), W, H, B)
        self.disp.show_progress('Start', 3)
        self.th = TempHumi(Pin(DHT))
        self.sgp = CO2TVOC(Pin(SCL), Pin(SDA))
        self.wireless = Wireless(WIFI_NAME, WIFI_PASSWORD)
        self.datetime = DateTime(self.wireless)
        self.logger = Logger(LOG_FILENAME)
        self.logger.write_startlog('\nSTART\n')

        self._count = 0
        self._boarder_state = True

    def measure(self):
        need_sync = True if self._count % SYNC_DURATION_COUNT == 0 else False
        need_log = True if self._count % LOG_DURATION_COUNT == 0 else False

        sync_stat = 0
        mark = ''
        if need_sync:
            self.disp.show_progress('Sync Time', 1)
            sync_stat = self.datetime.sync()
            if sync_stat == 1:
                self.disp.show_text('Sync Success')
                mark = '*'
            elif sync_stat == -1:
                self.disp.show_text('Connect Fail')
                mark = 'x'
            elif sync_stat == -2:
                self.disp.show_text('Sync Fail')
                mark = '-'

        firstline, secondline, datetimestr = self.datetime.get_formatted()

        if need_sync:
            self.logger.write_synclog(datetimestr, mark)

        temperature, humidity = self.th.measure()
        co2eq, tvoc = self.sgp.measure()

        thirdline = "T %2d.C  H %2d%%" % (temperature, humidity)
        forthline = "CO2 %3d ppm" % co2eq
        fifthline = "TVO %3d ppb" % tvoc

        self._boarder_state = not self._boarder_state

        self.disp.show_text(
            [firstline, secondline, thirdline, forthline, fifthline],
            self._boarder_state)

        if need_log:
            self.disp.show_progress('Write Log', 1)
            self.logger.write_datalog(datetimestr, temperature, humidity,
                                      co2eq, tvoc)

        if self._count and need_sync and need_log:
            self._count = 1
        else:
            self._count += 1

    # print(self._count)

    def measure_loop(self):
        # tim = Timer(-1)
        # try:
        #     tim.init(mode = Timer.PERIODIC, period = 3000 , callback = lambda t : self.measure())
        # except Exception:
        #     tim.deinit()
        while True:
            self.measure()
            time.sleep(DURATION_SECS)


if __name__ == '__main__':
    Station().measure_loop()
