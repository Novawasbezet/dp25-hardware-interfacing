from machine import Pin
import time

# LED outputs
led_groen = Pin(10, Pin.OUT)
led_geel = Pin(11, Pin.OUT)
led_rood = Pin(12, Pin.OUT)

# Start in veilige toestand
led_groen.value(1)
led_geel.value(0)
led_rood.value(0)

print("Systeem gestart, status veilig")

while True:
    time.sleep(0.5)
