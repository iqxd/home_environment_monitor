from display import Display
from machine import Pin, I2C, RTC
from temphumi import TempHumi
import sgp30
import network
import os
import time
import ntptime
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


def connect_wifi(wlan, init=False):
    wlan.connect(WIFI_NAME, WIFI_PASSWORD)
    if wlan.isconnected():
        return True
    for i in range(15):
        if wlan.isconnected():
            return True
        time.sleep(1)
    else:
        return False


def sync_time():
    try:
        ntptime.settime()
    except:
        return False
    else:
        return True


def write_startlog(start_message):
    with open(LOG_FILENAME, 'a') as f:
        f.write(start_message)


def write_titlelog():
    with open(LOG_FILENAME, 'a') as f:
        f.write('%4s %14s %2s %2s %4s %4s\n' %
                ('No.', 'Datetime', 'TC', 'H%', 'CO2', 'TVOC'))


def check_reset_log():
    try:
        logsize = os.stat(LOG_FILENAME)[6]
    except Exception:
        logsize = 0
    # print('logsize = %d' % logsize)
    if logsize > LOG_MAXBYTES:
        gc.collect()
        try:
            logs = read_datalog()
        except MemoryError:
            with open(LOG_FILENAME, 'w') as f:
                f.write('===Memory Allocation Error===')
            return
        lines = logs.split('\n')
        leftlines = lines[(len(lines) // 2):]
        with open(LOG_FILENAME, 'w') as f:
            f.write('\n'.join(leftlines))


def write_datalog(logno, logtimestr, temp, humi, co2, tvoc):
    #check_reset_log()
    with open(LOG_FILENAME, 'a') as f:
        if logno == 1:
            f.write('%4s %14s %2s %2s %4s %3s\n' %
                    ('No.', 'Datetime', 'TC', 'H%', 'CO2', 'TVOC'))
        f.write('%4d %14s %2d %2d %4d %3d\n' %
                (logno, logtimestr, temp, humi, co2, tvoc))


def write_synclog(logtimestr, sync):
    if sync > 0:
        mark = '*'
    elif sync == -1:
        mark = 'x'
    elif sync == -2:
        mark = '-'
    else:
        mark = ' '
    with open(LOG_FILENAME, 'a') as f:
        f.write('%4s %14s\n' % (mark, logtimestr))


def read_datalog():
    with open(LOG_FILENAME, 'r') as f:
        logs = f.read()
        # print(logs)
        return logs


def main():
    ap = network.WLAN(network.AP_IF)
    if ap.active():
        ap.active(False)
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    assert wlan.active()
    #wlan.scan()

    display = Display(Pin(DC), Pin(RES), Pin(CS), W, H, B)

    ntptime.NTP_DELTA = 3155644800
    ntptime.host = 'ntp1.aliyun.com'
    rtc = RTC()

    th = TempHumi(Pin(DHT))

    i2c = I2C(scl=Pin(SCL), sda=Pin(SDA), freq=100000)
    sgp = sgp30.Adafruit_SGP30(i2c)

    logno = -1

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

    blinkcount = 0
    synccount = 0
    logcount = 1  # not log at start time ; 0 if log data at start time

    display.show_progress('Start', 3)
    while True:
        sync = 0
        if synccount % SYNC_SECS == 0:
            display.show_progress('Sync Time', 1)
            if connect_wifi(wlan):
                for i in range(3):
                    if sync_time():
                        rtc = RTC()
                        sync = 1
                        display.show_text('Sync Success')
                        break
                    time.sleep(1)
                else:
                    sync = -2
                    display.show_text('Sync Fail')
            else:
                sync = -1
                display.show_text('Connect Fail')
            time.sleep_ms(500)
            synccount = 0
        synccount += 1

        year, month, day, weekday, hour, minute, second, _ = rtc.datetime()
        firstline = "%s %02d %s %d" % (weekdays[weekday + 1], day,
                                       months[month], year)
        secondline = "%02d:%02d:%02d" % (hour, minute, second)
        datetimestr = '%04d%02d%02d%02d%02d%02d' % (year, month, day, hour,
                                                    minute, second)

        if logno == -1:
            # write start message
            write_startlog('\nSTART\n')
            logno = 0

        if sync != 0:
            write_synclog(datetimestr, sync)

        # measure temperature and humidity
        temperature, humidity = th.measure()
        thirdline = "T %2d.C  H %2d%%" % (temperature, humidity)

        co2eq, tvoc = sgp.iaq_measure()
        forthline = "CO2 %3d ppm" % co2eq
        fifthline = "TVO %3d ppb" % tvoc

        if blinkcount % BLINK_SECS == 0:
            boarder_state = True  # boarder on
            blinkcount = 0
        else:
            boarder_state = False  # boarder off
        blinkcount += 1

        display.show_text(
            [firstline, secondline, thirdline, forthline, fifthline],
            boarder_state)

        if logcount % LOG_SECS == 0:
            logno += 1
            display.show_progress('Write Log', 1)
            write_datalog(logno, datetimestr, temperature, humidity, co2eq,
                          tvoc)
            logcount = 0
        logcount += 1

        time.sleep(1)


main()
