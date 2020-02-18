import RPi.GPIO as GPIO
import time
import picamera

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
PIR_PIN = 7
GPIO.setup(PIR_PIN, GPIO.IN)
BUZZER_PIN = 11
GPIO.setup(BUZZER_PIN,GPIO.OUT)

camera = picamera.PiCamera()
def picamera():
    camera.vflip = True
    camera.capture('frame1.jpg')
    camera.capture('frame2.jpg')
    camera.capture('frame3.jpg')
    print("Images taken")

p = GPIO.PWM(BUZZER_PIN, 100)
def buzzer():
        GPIO.output(BUZZER_PIN, True)
        p.start(100)
        p.ChangeDutyCycle(90)
        p.ChangeFrequency(400)
        time.sleep(5)
        p.stop()

def objectdetection(input_image):
    import cv2
    import numpy as np

    #Load yolo
    net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
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
            if confidence > 0.5:
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
                return object

try:
    time.sleep(1)
    print("Ready for operation")
    while True:
        if GPIO.input(PIR_PIN):
            print("Motion detected")
            print("Activate picamera")
            picamera()
            obj_detec_result = objectdetection('frame1.jpg')
        time.sleep(1)
except KeyboardInterrupt:
    print("Quit")
    GPIO.cleanup()
