from machine import PIN,I2C,SPI,RTC
import ssd1306
import dht
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
SYNC_SECS = 1200 # 600
LOG_SECS = 120  # 300 # 50k generated one day if log every 60 second
LOG_FILENAME = 'timelog.txt' 
# LOG_MAXBYTES = 1024 * 2  

# hardware GPIO pins
# D1 Mini Board
DC=2   # D4
RES=0   # D3
CS=15  # D8
DHT=12  # D6
SCL=5   # D1
SDA=4   # D2


def clear_screen(oled):
    oled.fill(0)


def clear_content(oled):
    oled.fill_rect(B, B, W - B * 2, H - B * 2, 0)


def fill_boarder(oled , state):
    if state:
        onoff = 1
    else:
        onoff = 0
    oled.fill_rect(0, 0, W, B, onoff)
    oled.fill_rect(0, H - B, W, B, onoff)
    oled.fill_rect(0, 0, B, H, onoff)
    oled.fill_rect(W - B, 0, B, H, onoff)


def fill_text(oled, text, lineno=1, linecount=1):
    nchar = len(text)
    # print(nchar)
    assert (W - B * 2) / nchar > 8
    assert (H - B * 2) / linecount > 8
    wpixels = nchar * 8
    x = W / 2 - wpixels / 2
    y = ((H - B * 2) / linecount) * (lineno - 1 / 2) + B - 4
    oled.text(text, int(x), int(y))
    

def show_progress(oled, text, secs):
    padding = 10
    expand_count_per_sec = 5
    duration_ms = 1000 // expand_count_per_sec
    count = secs * expand_count_per_sec # expand 5 times per second
    bw = (W - B * 2 - padding * 2) // count  # now secs should <= 21 s
    assert bw > 0
    fill_boarder(oled , True)
    clear_content(oled)
    fill_text(oled, text, 1, 2)

    x = int(B + padding)
    y = int((H - B * 2) / 2 * (2 - 1 / 2) + B - 4)

    for i in range(count):
        oled.fill_rect(x + i * bw, y, bw, 8, 1)
        oled.show()
        time.sleep_ms(duration_ms)


def show_message(oled, text, boarder=True):
    # text : str or list[str] ,  boarder : bool
    fill_boarder(oled,boarder)
    clear_content(oled)    
    if isinstance(text , str):
        text = [text]
    linecount = len(text)
    for lino,chs in enumerate(text,1):
        fill_text(oled, chs, lino, linecount)
    oled.show()

def connect_wifi(wlan , init = False):
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
        f.write('%4s %14s %2s %2s %4s %4s\n' % ('No.','Datetime','TC','H%','CO2','TVOC'))


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


def write_datalog(logno, logtimestr, temp,humi,co2,tvoc):
    #check_reset_log()
    with open(LOG_FILENAME, 'a') as f:
        if logno == 1:
            f.write('%4s %14s %2s %2s %4s %3s\n' % ('No.','Datetime','TC','H%','CO2','TVOC'))
        f.write('%4d %14s %2d %2d %4d %3d\n' % (logno,logtimestr,temp,humi,co2,tvoc))

def write_synclog(logtimestr,sync):
    if sync >0 :
        mark = '*'
    elif sync == -1:
        mark = 'x'
    elif sync == -2:
        mark = '-'
    else:
        mark = ' '
    with open(LOG_FILENAME, 'a') as f:
        f.write('%4s %14s\n' % (mark,logtimestr))

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
    
    spi = SPI(1, baudrate=8000000, polarity=0, phase=0)
    oled = ssd1306.SSD1306_SPI(128, 64, spi, PIN(DC), PIN(RES),
                               PIN(CS))

    ntptime.NTP_DELTA = 3155644800
    ntptime.host = 'ntp1.aliyun.com'
    rtc = RTC()

    th = dht.DHT11(PIN(DHT))
    
    i2c = I2C(scl= PIN(SCL),sda=PIN(SDA),freq=100000)
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
    
    show_progress(oled, 'Start', 3)
    while True:
        sync = 0
        if synccount % SYNC_SECS == 0:
            show_progress(oled, 'Sync Time', 1)
            if connect_wifi(wlan):          
                for i in range(3):
                    if sync_time():
                        rtc = RTC()
                        sync = 1
                        show_message(oled, 'Sync Success')
                        break
                    time.sleep(1)
                else:
                    sync = -2
                    show_message(oled, 'Sync Fail')       
            else:
                sync = -1
                show_message(oled, 'Connect Fail')
            time.sleep_ms(500)
            synccount = 0
        synccount += 1

        year, month, day, weekday, hour, minute, second, _ = rtc.datetime()
        firstline = "%s %02d %s %d" % (weekdays[weekday + 1], day,
                                       months[month], year)
        secondline = "%02d:%02d:%02d" % (hour, minute, second)  
        datetimestr = '%04d%02d%02d%02d%02d%02d' % (year,month,day,hour,minute,second)
        
        if logno == -1:
            # write start message
            write_startlog('\nSTART\n')
            logno = 0
        
        if sync != 0:
            write_synclog(datetimestr,sync)


        # measure temperature and humidity
        th.measure()
        temperature = th.temperature()
        humidity = th.humidity()
        thirdline = "T %2d.C  H %2d%%" % (temperature, humidity)
        
        co2eq, tvoc = sgp.iaq_measure()
        forthline = "CO2 %3d ppm" % co2eq
        fifthline = "TVO %3d ppb" % tvoc
        
        if blinkcount % BLINK_SECS == 0:
            boarder_state = True   # boarder on
            blinkcount = 0
        else :
            boarder_state = False  # boarder off
        blinkcount += 1

        show_message(oled,[firstline,secondline,thirdline,forthline,fifthline],boarder_state)

        if logcount % LOG_SECS == 0:
            logno += 1
            show_progress(oled, 'Write Log', 1)
            write_datalog(logno,datetimestr,temperature,humidity,co2eq,tvoc)
            logcount = 0
        logcount += 1

        time.sleep(1)


main()
