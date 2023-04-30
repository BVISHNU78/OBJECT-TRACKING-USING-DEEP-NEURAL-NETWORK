import cv2
from gui_buttons import Buttons
import numpy as np
import argparse
button = Buttons()
button.add_button("person",10,20)
button.add_button("cell phone", 10, 100)
button.add_button("keyboard", 10, 180)
button.add_button("remote", 10, 260)
button.add_button("scissors", 10, 340)
button.add_button("pen",10,400)
colors =button.colors
ap = argparse.ArgumentParser()
neted = cv2.dnn.readNet("dnn_model/yolov4-tiny.cfg","dnn_model/yolov4-tiny.weights")
model = cv2.dnn_DetectionModel(neted)
model.setInputParams(size=(320,320),scale=1/255)
classes =[]
with open("dnn_model/classes.txt",) as file_object:
    for class_name in file_object.readlines():
        class_name =class_name.strip()
        classes.append(class_name)
    print("object list")
    print(classes[0])
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH ,1080)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)

def click_button(event,x,y,flags,params):
    global button_person
    if event == cv2.EVENT_LBUTTONDOWN:
        button.button_click(x,y)
          
cv2.namedWindow("FRAME")
cv2.setMouseCallback("FRAME",click_button)
while True:
    ret,frame =cap.read()
    
    active_buttons =button.active_buttons_list()
    print("ACTIVE buttons",active_buttons)
    (class_ids,scores,bboxes) = model.detect(frame)
    for class_id ,score ,bbox in zip(class_ids,scores,bboxes):
        (x,y,w,h)=bbox
        #print(x,y,w,h)
        class_name =classes[class_id]
        color =colors[class_id]
        
        if class_name in active_buttons:
            cv2.putText(frame,str(class_name),(x,y - 5),cv2.FONT_HERSHEY_PLAIN,2,(0,255,255),2)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(200,0,255),2)
    #print("Class_ids",class_ids)
    #print("scores",scores)
    #print("bboxes",bboxes)
    #create a box
    #cv2.rectangle(frame,(30,30),(200,90),(255,0,255),-1)
    button.display_buttons(frame)
    cv2.imshow("FRAME",frame)
    cv2.waitKey(1)
videoCapture.release()
cv2.destroyAllWindows()

cap.release()
cv2.destroyAllWindows()