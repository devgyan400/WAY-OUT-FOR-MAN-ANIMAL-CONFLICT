import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
FIRE_PIN = 7
GPIO.setmode(GPIO.BOARD)
GPIO.setup(FIRE_PIN,GPIO.IN)

try:
    while True:
        time.sleep(1)
        if GPIO.input(FIRE_PIN):
            print("Flame detected")
        else:
            print("Flame not detected")
except KeyboardInterrupt:
    print("Quit")
    GPIO.cleanup()
