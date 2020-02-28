import RPi.GPIO as GPIO
import time
from Adafruit_CharLCD import Adafruit_CharLCD

lcd = Adafruit_CharLCD(rs=26, en=19, d4=13, d5=6, d6=5, d7=21, cols=16, lines=2)
lcd.clear()
lcd.message("Ready for \n operation")
time.sleep()
lcd.clear()