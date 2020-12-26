import RPi.GPIO as GPIO
import time

relay_pin = 21

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_pin, GPIO.OUT)


def relay_on(pin):
    GPIO.output(pin, GPIO.HIGH)  # Turn relay on


def relay_off(pin):
    GPIO.output(pin, GPIO.LOW)  # Turn relay off


if __name__ == '__main__':
    try:
        relay_on(relay_pin)
        time.sleep(1)
        relay_off(relay_pin)
        time.sleep(1)
        GPIO.cleanup()
    except KeyboardInterrupt:
        GPIO.cleanup()