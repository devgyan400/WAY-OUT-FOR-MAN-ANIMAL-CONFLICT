import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)

p = GPIO.PWM(11, 100)

def buzzer():
        GPIO.output(11, True)
        p.start(100)
        p.ChangeDutyCycle(50)
        p.ChangeFrequency(400)
        time.sleep(5)
        p.stop()
buzzer()