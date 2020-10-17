# AirQualityWatcher
an air quality watcher based on esp8266 and micropython

## Hardware
1. D1 Mini board with esp8266 chip
2. SSD1306, 0.96 inch , 7 pin OLED Screen
3. DHT11, Temperature and Humidity Sensor 
4. SGP30, CO2 and TVOC Sensor

## Connection
| D1 Mini Label | ESP8266 GPIO | SSD1306 | DHT11 | SGP30 |
| ----|   ----    |----|----|----| 
| D0  | GPIO16    |    |    |    | 
| D1  | GPIO5     |    |    |SCL | 
| D2  | GPIO4     |    |    |SDA | 
| D3  | GPIO0     | RES|    |    | 
| D4  | GPIO2     | DC |    |    | 
| D5  | GPIO14    | D0 |    |    | 
| D6  | GPIO12    |    |OUT |    | 
| D7  | GPIO13    | D1 |    |    | 
| D8  | GPIO15    | CS |    |    | 
| RX  | GPIO3/RXD |    |    |    | 
| TX  | GPIO1/TXD |    |    |    | 
| A0  | ADC0      |    |    |    | 
| G   | GND       |GND | -  |GND | 
| 5V  |           |    |    |    | 
| 3V3 | 3.3V      |VCC | +  |VCC | 
| RST | RST       |    |    |    | 

