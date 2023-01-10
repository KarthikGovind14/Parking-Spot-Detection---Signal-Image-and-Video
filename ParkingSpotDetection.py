import cv2
import pickle
import numpy as np

# Video feed
cap = cv2.VideoCapture('CrowdedParking.mp4')
 
with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)
 
width, height = 35, 70
full = width * height
empty = 0.22
font = cv2.FONT_HERSHEY_COMPLEX_SMALL
font2 = cv2.FONT_HERSHEY_DUPLEX

 
def checkParkingSpace(imgPro):
    spaceCounter = 0
    
 
    for pos in posList:
        x, y = pos
 
        imgCrop = imgPro[y:y + height, x:x + width]
     
        count = cv2.countNonZero(imgCrop)
      
        # condition for pixel count inside the marked space

        if count < 680:
             color = (0, 255, 0)
             thickness = 2
             spaceCounter += 1
             
        else:
             color = (0, 0, 255)
             thickness = 2
            
        # placing the rectangular space collected from the list 

        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)

        # pixel count on each rectangualr space
        # cv2.putText(img, str(count),(x, y), font, 0.7, (255, 255, 255), 1, cv2.LINE_AA)

        # Draw black background rectangle
        cv2.rectangle(img, (1100, 20), (1336, 80), (0,0,0), -1)
       
        cv2.putText(img, f'Free: {(spaceCounter)}/{len(posList)}' , (1100, 70), font2, 1.2, (0,200,0), 2, cv2.LINE_4)
        # cv2.imshow(str(x * y), imgCrop)
       
while True:

    
    #looping the video depending on the frames of the input video
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    
    success, img = cap.read()
    #Frame Processing
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    #auto thresholding is done to find pixels in the slot by which it can define the slot is emty
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)
                                         
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)
   
   # Function for finding the count of the available parking lots
    checkParkingSpace(imgDilate)
  

    cv2.imshow("Image", img)
    # cv2.imshow("ImageBlur", imgBlur)
    # cv2.imshow("ImageThres", imgMedian)
    cv2.waitKey(10)