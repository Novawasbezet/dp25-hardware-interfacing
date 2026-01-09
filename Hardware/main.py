from machine import Pin, PWM
import time

# LED outputs
led_groen = Pin(10, Pin.OUT)
led_geel = Pin(11, Pin.OUT)
led_rood = Pin(12, Pin.OUT)

zoemer = PWM(Pin(13))
zoemer.deinit()

# Inputs
tiltsensor = Pin(4, Pin.IN, Pin.PULL_UP)
reset_knop = Pin(14, Pin.IN, Pin.PULL_UP)

# Tijdgrenzen
RISICO_TIJD = 3000
GEVAAR_TIJD = 5000
AFWIJKING_TIMEOUT = 800

status = "VEILIG"
start_afwijking = None
laatste_beweging = None

# Start veilig
led_groen.value(1)

# Status functies
def status_veilig():
    led_groen.value(1)
    led_geel.value(0)
    led_rood.value(0)
    zoemer.deinit()

def status_risico():
    led_groen.value(0)
    led_geel.value(1)
    led_rood.value(0)
    zoemer.deinit()

def status_gevaar():
    led_groen.value(0)
    led_geel.value(0)
    led_rood.value(1)
    zoemer.init(freq=2000, duty_u16=30000)

status_veilig()
print("Systeem gestart, status: VEILIG")

while True:
    nu = time.ticks_ms()

    if status == "GEVAAR":
        if reset_knop.value() == 0:
            print("Reset uitgevoerd door onderhoud")
            status = "VEILIG"
            start_afwijking = None
            laatste_beweging = None
            status_veilig()
            time.sleep(0.5)
        time.sleep(0.05)
        continue

    if tiltsensor.value() == 1:
        laatste_beweging = nu
        if start_afwijking is None:
            start_afwijking = nu
            print("Afwijking gestart")

    afwijking_actief = False
    if laatste_beweging is not None:
        if time.ticks_diff(nu, laatste_beweging) < AFWIJKING_TIMEOUT:
            afwijking_actief = True

    if afwijking_actief:
        duur = time.ticks_diff(nu, start_afwijking)

        if duur >= GEVAAR_TIJD:
            status = "GEVAAR"
            status_gevaar()
            print("Status: GEVAAR")

        elif duur >= RISICO_TIJD:
            status = "RISICO"
            status_risico()
            print("Status: RISICO")

    else:
        start_afwijking = None
        laatste_beweging = None
        status = "VEILIG"
        status_veilig()

    time.sleep(0.05)