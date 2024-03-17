import cv2
import numpy as np

# Web Camera section
video_path = r'C:\Users\PC\OneDrive\Desktop\Veichle_tracer\Resource\video.mp4'
cap = cv2.VideoCapture(video_path)

#Count line position
count_line_position = 550
min_width_rectangle = 80
min_height_rectangle = 80

#for minimum error between pixel
offset = 6

# for counting veichle
counter = 0

#Initialize subtractor
algo = cv2.createBackgroundSubtractorMOG2()

def center_handle(x,y,w,h):
    x1 = int(w/2)
    y1 = int(h/2)
    cx = x+x1
    cy = y+y1
    return cx,cy

detect = []

while True:
    ret, frame1 = cap.read()
    
    grey = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey , (3,3) , 5)
    
    # applying on each frame
    img_sub = algo.apply(blur)
    dilate = cv2.dilate(img_sub,np.ones((5,5)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    
    dilateada = cv2.morphologyEx(dilate,cv2.MORPH_CLOSE,kernel)
    dilateada = cv2.morphologyEx(dilateada,cv2.MORPH_CLOSE,kernel)
    
    counter_shape, h = cv2.findContours(dilateada,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cv2.line(frame1,(25,count_line_position),(1200,count_line_position),(255,127,0),3)
    
    # for identifying each veichle
    for (i,c) in enumerate(counter_shape):
        (x,y,w,h) = cv2.boundingRect(c)
        validate_counter = (w >= min_width_rectangle) and (h >= min_height_rectangle)
        
        if not validate_counter:
            continue  
        
        cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,0),2)
        center = center_handle(x,y,w,h)
        detect.append(center)
        cv2.circle(frame1,center,4,(0,0,255),-1)     
        
        for (x,y) in detect:
            if y<(count_line_position+offset) and y>(count_line_position-offset):
                counter += 1
            cv2.line(frame1,(25,count_line_position),(1200,count_line_position),(0,127,255),3)
            detect.remove((x,y))
            print("Veichle Counter : "+str(counter))
            
    cv2.putText(frame1,"VEICHLE COUNTER :"+str(counter),(450,70),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),5) 
            
    # cv2.imshow('Detector',dilateada)
    cv2.imshow('Original Video',frame1)
    
    if cv2.waitKey(40) == 13:
        break
    
cv2.destroyAllWindows()
cap.release()