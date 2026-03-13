import cv2

for i in range(10):
    cap = cv2.VideoCapture(i)
    if cap.read()[0]:
        print("Camera works at index:", i)
        cap.release()


#https://mediapipe-studio.webapps.google.com/demo/hand_landmarker