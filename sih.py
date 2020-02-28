import RPi.GPIO as GPIO
import time
import picamera
from Adafruit_CharLCD import Adafruit_CharLCD

GPIO.setwarnings(False)
PIR_PIN = 27
GPIO.setup(PIR_PIN, GPIO.IN)
BUZZER_PIN = 22
GPIO.setup(BUZZER_PIN,GPIO.OUT)

list = ['person','boar','bear','monkey','elephant','horse','cat','dog','cow','leopard','tractor']

lcd = Adafruit_CharLCD(rs=26, en=19, d4=13, d5=6, d6=5, d7=21, cols=16, lines=2)
lcd.clear()

camera = picamera.PiCamera()
def picamera():
    camera.vflip = True
    camera.capture('frame1.jpg')
    camera.capture('frame2.jpg')
    camera.capture('frame3.jpg')
    print("Images taken")
    lcd.clear()
    lcd.message('Images taken')

p = GPIO.PWM(BUZZER_PIN, 100)
def buzzer(req_freq):
        GPIO.output(BUZZER_PIN, True)
        p.start(100)
        p.ChangeDutyCycle(90)
        p.ChangeFrequency(req_freq)
        lcd.message("\n"+str(req_freq)+"Hz")
        time.sleep(10)
        p.stop()

def objectdetection(input_image):
    import cv2
    import numpy as np

    det_list = []
    #Load yolo
    net = cv2.dnn.readNet("yolov3-tiny.weights", "yolov3-tiny.cfg")
    classes = []
    with open("coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))

    # Loading image
    img = cv2.imread(input_image)
    img = cv2.resize(img, None, fx=0.4, fy=0.4)
    height, width, channels = img.shape

    # Detecting objects
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

    net.setInput(blob)
    outs = net.forward(output_layers)

    # Showing informations on the screen
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.20:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
                object = classes[class_id]
                det_list.append(object)
    return det_list

try:
    time.sleep(2)
    print("Ready for operation")
    lcd.message("Ready for \n operation")
    time.sleep(2)
    while True:
        if GPIO.input(PIR_PIN):
            print("Motion detected")
            lcd.clear()
            lcd.message("Motion \n detected")
            time.sleep(2)
            print("Activate picamera")
            lcd.clear()
            lcd.message("Activate \n picamera")
            picamera()
            result = objectdetection('frame1.jpg')
            print(result)
            if result != None:
                for i in result:
                    lcd.clear()
                    lcd.message(i)
                    if i in list:
                            if i == 'person':
                                lcd.message("\n"+"pass")
                                time.sleep(10)
                            if i == 'bear':
                                buzzer(34000)
                            if i == 'boar':
                            	buzzer(34000)
                            if i == 'elephant':
                                buzzer(12000)
                            if i == 'monkey':
                                buzzer(42000)
                            if i == 'horse':
                                buzzer(24000)
                            if i == 'dog':
                                buzzer(32000)
                            if i == 'cat':
                                buzzer(32000)
                            if i == 'cow':
                            	buzzer(35000)
                            if i == 'leopard':
                                buzzer(45000)
                            if i == 'tractor':
                                lcd.message("\n"+"pass")
                                time.sleep(10)
                lcd.clear()
        time.sleep(2)
except KeyboardInterrupt:
    print("Exit")
    lcd.message("Exit")
    time.sleep(2)
    lcd.clear()
    GPIO.cleanup()
