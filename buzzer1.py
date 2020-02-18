import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)

p = GPIO.PWM(11, 100)

try:
    while True:
        GPIO.output(11, True)
        p.start(100)
        p.ChangeDutyCycle(50)
        p.ChangeFrequency(400)
  
except KeyboardInterrupt:
    print("Quit")
    GPIO.cleanup()