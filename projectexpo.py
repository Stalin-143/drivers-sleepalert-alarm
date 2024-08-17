import cv2
import numpy as np
import winsound
import threading
import time

# Load pre-trained Haar cascade for face and eye detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Check if the cascades are loaded properly
if face_cascade.empty() or eye_cascade.empty():
    print("Error loading Haar cascades.")
    exit(1)

# Load the webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit(1)

# Beep control
beep_running = False

def beep():
    global beep_running
    while beep_running:
        winsound.Beep(1000,1000)
        time.sleep(0.1)

beep_thread = None

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    eyes_detected = False
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]

        eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 22)
        for (ex, ey, ew, eh) in eyes:
            if ey + eh/2 < h/2:  # Ensuring that eyes are in the upper half of the face rectangle
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
                eyes_detected = True

    if eyes_detected:
        if beep_running:
            beep_running = False
            if beep_thread:
                beep_thread.join()
            beep_thread = None
    else:
        if not beep_running:
            beep_running = True
            beep_thread = threading.Thread(target=beep)
            beep_thread.start()

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
beep_running = False
if beep_thread:
    beep_thread.join()
cap.release()
cv2.destroyAllWindows()