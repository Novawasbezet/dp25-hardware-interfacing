from machine import Pin
import time

# LED outputs
led_groen = Pin(10, Pin.OUT)
led_geel = Pin(11, Pin.OUT)
led_rood = Pin(12, Pin.OUT)

# Inputs
tiltsensor = Pin(4, Pin.IN, Pin.PULL_UP)
reset_knop = Pin(14, Pin.IN, Pin.PULL_UP)

# Start veilig
led_groen.value(1)
led_geel.value(0)
led_rood.value(0)

print("Systeem gestart, status veilig")

while True:
    if tiltsensor.value() == 1:
        print("Afwijking gedetecteerd")
        led_groen.value(0)
        led_geel.value(1)

    if reset_knop.value() == 0:
        led_groen.value(1)
        led_geel.value(0)

    time.sleep(0.2)