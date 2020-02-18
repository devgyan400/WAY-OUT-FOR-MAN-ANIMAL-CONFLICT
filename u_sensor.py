import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
TRIG_PIN = 7
GPIO.setup(TRIG_PIN,GPIO.OUT)
ECHO_PIN = 11
GPIO.setup(ECHO_PIN,GPIO.IN)

try:
    while True:
        GPIO.output(TRIG_PIN, GPIO.LOW)
        print("Waiting for sensor to settle")
        time.sleep(2)

        GPIO.output(TRIG_PIN, True)
        time.sleep(0.00001)
        GPIO.output(TRIG_PIN, False)

        while GPIO.input(ECHO_PIN) == 0:
            StartTime = time.time()
        while GPIO.input(ECHO_PIN) == 1:
            StopTime = time.time()

        TimeElapsed = StopTime - StartTime
        distance = round(TimeElapsed*17150, 2)
        print(distance)
        time.sleep(1)

except KeyboardInterrupt:
    print("Quit")
    GPIO.cleanup()
