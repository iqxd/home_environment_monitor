from machine import Pin
from wireless import Wireless
from datetime import DateTime
from display import Display
from temphumi import TempHumi
from co2tvoc import CO2TVOC
from logger import Logger
import os
import time
import gc

# constants
W = 128
H = 64
B = 2
WIFI_NAME = 'wifiname'
WIFI_PASSWORD = 'wifipassword'
BLINK_SECS = 3
SYNC_SECS = 1200  # 600
LOG_SECS = 120  # 300 # 50k generated one day if log every 60 second
LOG_FILENAME = 'timelog.txt'
LOG_MAXBYTES = 1024 * 2

# hardware GPIO Pins
# D1 Mini Board
DC = 2  # D4
RES = 0  # D3
CS = 15  # D8
DHT = 12  # D6
SCL = 5  # D1
SDA = 4  # D2


def main():
    disp = Display(Pin(DC), Pin(RES), Pin(CS), W, H, B)
    disp.show_progress('Start', 3)
    th = TempHumi(Pin(DHT))
    sgp = CO2TVOC(Pin(SCL), Pin(SDA))
    wireless = Wireless(WIFI_NAME,WIFI_PASSWORD)
    datetime = DateTime(wireless)
    logger = Logger(LOG_FILENAME)

    logno = -1

    blinkcount = 0
    synccount = 0
    logcount = 1  # not log at start time ; 0 if log data at start time

    while True:
        sync = 0
        if synccount % SYNC_SECS == 0:
            disp.show_progress('Sync Time', 1)
            sync = datetime.sync()
            if sync == 1:
                disp.show_text('Sync Success')
            elif sync == -1:
                disp.show_text('Connect Fail')
            elif sync == -2:
                disp.show_text('Sync Fail')
            time.sleep_ms(500)
            synccount = 0
        synccount += 1

        firstline,secondline,datetimestr = datetime.get_formatted()

        if logno == -1:
            # write start message
            logger.write_startlog('\nSTART\n')
            logno = 0

        if sync != 0:
            logger.write_synclog(datetimestr, sync)

        # measure temperature and humidity
        temperature, humidity = th.measure()
        thirdline = "T %2d.C  H %2d%%" % (temperature, humidity)

        co2eq, tvoc = sgp.measure()
        forthline = "CO2 %3d ppm" % co2eq
        fifthline = "TVO %3d ppb" % tvoc

        if blinkcount % BLINK_SECS == 0:
            boarder_state = True  # boarder on
            blinkcount = 0
        else:
            boarder_state = False  # boarder off
        blinkcount += 1

        disp.show_text(
            [firstline, secondline, thirdline, forthline, fifthline],
            boarder_state)

        if logcount % LOG_SECS == 0:
            logno += 1
            disp.show_progress('Write Log', 1)
            logger.write_datalog(logno, datetimestr, temperature, humidity, co2eq,
                          tvoc)
            logcount = 0
        logcount += 1

        time.sleep(1)


main()
