import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
PIR_PIN = 7
GPIO.setup(PIR_PIN, GPIO.IN)

try:
    time.sleep(1)
    print("Ready for operation")
    while True:
        if GPIO.input(PIR_PIN):
            print("Motion detected")
        else:
            print("Motion not detected")
        time.sleep(1)
except KeyboardInterrupt:
    print("Quit")
    GPIO.cleanup()
