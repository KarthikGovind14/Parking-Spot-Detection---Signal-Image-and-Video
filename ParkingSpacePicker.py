
import cv2
import pickle
 
# W&H of the shape 
width, height = 35, 70
 
# for prechecking the object if there are exciting marked slots in the loaded image 
try:
    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []
 
# mouse click event to capture the parking slots 
def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)
 
    with open('CarParkPos', 'wb') as f:
        pickle.dump(posList, f)
 
# loop the image again to make rectangular mark  
while True:
    img = cv2.imread('parkingLot.png')
    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)
 
    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", mouseClick)
    cv2.waitKey(1)