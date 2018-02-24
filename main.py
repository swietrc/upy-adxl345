import utime
import ustruct
import usocket
import gc
from adxl345 import ADXL345
from machine import Pin, I2C

led = Pin(14, Pin.OUT)
i2c = I2C(sda=Pin(4), scl=Pin(0))
adxl = ADXL345(i2c)

s = usocket.socket(usocket.AF_INET, usocket.SOCK_DGRAM)
buf = bytearray()

def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid, passwd)
        while not sta_if.isconnected():
            pass
    network.WLAN(network.AP_IF).active(False)
    print('network config: ', sta_if.ifconfig())

def send_data():
    global buf
    s.sendto(buf, ("192.168.43.61", 6667))
    buf = bytearray(0)
    gc.collect()

def main():
    global buf
    i = 0
    buf = bytearray()
    while i < 5000:
        led.value(i%2)
        x, y, z = adxl.read()
        buf = buf + ustruct.pack('ibbb', utime.ticks_ms(), x, y, z)
        if (len(buf) + 7) > 300:
            send_data()
        utime.sleep_ms(10)
        i = i + 1

do_connect()
main()
led.off()
