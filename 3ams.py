import RPi.GPIO as GPIO
import time


# enable debugging info
debug = True
# set GPIO to use physical pin numbers
GPIO.setmode(GPIO.BOARD)
# define pin to LDR, default 7
ldr_pin = 7
relay_pin = 40
# measurement interval in milliseconds. Higher interval improves accuracy
# default: 20000
interval = 10000

# read file and set prices
f = open('priser.txt', 'r')
f = f.readlines()
nettleie = round(float(f[0])/100.0, 3)
kWhpris = round(float(f[1])/100.0, 3)
fastledd = float(f[2])

def relay_on(pin):
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(0.05)

def relay_off(pin):
    GPIO.output(pin, GPIO.LOW)
    time.sleep(0.05)

def setPrices():
    pass

def getPrices():
    pass

def rc_time(ldr_pin):
    count = 0

    GPIO.setup(ldr_pin, GPIO.OUT)
    GPIO.output(ldr_pin, GPIO.LOW)
    time.sleep(0.1)

    GPIO.setup(ldr_pin, GPIO.IN)

    while (GPIO.input(ldr_pin) == GPIO.LOW):
        count += 1
    
    return count

def start_reading(ldr_pin, interval):
    print("START_READING")
    measurement_count = 0
    try:
        while True:
            start_time = int(round(time.time() * 1000))
            t = start_time
            count = 0

            while (start_time + interval >= t):
                if (rc_time(ldr_pin) < 20000):
                    count += 1
                    relay_off(relay_pin)
                relay_on(relay_pin)
                t = time.time() * 1000

            hourly_pulse = round(count * 3 * 60, 2)
            hourly_cost = round(hourly_pulse * (kWhpris / 1000), 2)
            monthly_cost = round(hourly_cost * 24 * 30 + fastledd, 2)

            measurement_count += 1

            print(time.strftime('%H:%M:%S'))
            if debug:
                print('---------------------')
                print(f'MEASURE_COUNT: {measurement_count}')
                print(f'PULSES_COUNT: {count}')
                print()
                print(f'FORBRUK_SISTE_{int(interval/1000)} S: {hourly_pulse} Wh')
                print(f'TIMEPRIS_: {hourly_cost} kr')
                print(f'DAGSPRIS_: {hourly_cost*24+fastledd/30} kr')
                print(f'MÅNEDSSPRIS_: {monthly_cost} kr')

    except KeyboardInterrupt as e:
        print('KeyboardInterrupt')
        GPIO.cleanup()


def main():
    GPIO.setup(relay_pin, GPIO.OUT)

    start_reading(ldr_pin=ldr_pin, interval=interval)

if __name__ == '__main__':
    main()