# Home Environment Monitor
IOT home environment monitor based on esp8266 and micropython

## Hardware
1. D1 Mini board with esp8266 chip
2. SSD1306, 0.96 inch 128x64 pixels, 7 pin OLED Screen
3. DHT11, Temperature and Humidity Sensor 
4. SGP30, CO2 and TVOC Sensor

### Connection
| D1 Mini Pin | ESP8266 Pin | SSD1306 | DHT11 | SGP30 |
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


## Firmware
MicroPython v1.13 2020-09-11; ESP module with ESP8266

## Communication
MQTT Protocal with Broker Emqx

## Upper Monitor Gui
Dear PyGui 0.5.66 
CPython 3.8

## Prototype
![avatar](https://user-images.githubusercontent.com/13008913/99083762-f3f97700-2600-11eb-96b4-054dbdca560f.jpg)

## Realtime Monitor
![avatar](https://user-images.githubusercontent.com/13008913/99083683-d5937b80-2600-11eb-8443-9e8a42945c07.PNG)
