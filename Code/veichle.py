import cv2
import numpy as np

# Web Camera section
video_path = r'C:\Users\PC\OneDrive\Desktop\Veichle_tracer\Resource\video.mp4'
cap = cv2.VideoCapture(video_path)

while True:
    ret, frame1 = cap.read()
    cv2.imshow('Original video',frame1)
    
    if cv2.waitKey(1) == 13:
        break
    
cv2.destroyAllWindows()
cap.release()