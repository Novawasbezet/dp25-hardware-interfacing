from machine import Pin
import time

# LED outputs
led_groen = Pin(10, Pin.OUT)
led_geel = Pin(11, Pin.OUT)
led_rood = Pin(12, Pin.OUT)

# Inputs
tiltsensor = Pin(4, Pin.IN, Pin.PULL_UP)
reset_knop = Pin(14, Pin.IN, Pin.PULL_UP)

# Tijdgrenzen
RISICO_TIJD = 3000
GEVAAR_TIJD = 5000

status = "VEILIG"
start_afwijking = None

# Start veilig
led_groen.value(1)

print("Systeem gestart, status veilig")

while True:
    nu = time.ticks_ms()

    if tiltsensor.value() == 1:
        if start_afwijking is None:
            start_afwijking = nu

        duur = time.ticks_diff(nu, start_afwijking)

        if duur >= GEVAAR_TIJD:
            status = "GEVAAR"
            led_rood.value(1)
            led_geel.value(0)
            led_groen.value(0)

        elif duur >= RISICO_TIJD:
            status = "RISICO"
            led_geel.value(1)
            led_groen.value(0)

    else:
        start_afwijking = None
        status = "VEILIG"
        led_groen.value(1)
        led_geel.value(0)
        led_rood.value(0)

    if status == "GEVAAR" and reset_knop.value() == 0:
        status = "VEILIG"
        start_afwijking = None
        led_groen.value(1)
        led_rood.value(0)

    time.sleep(0.1)