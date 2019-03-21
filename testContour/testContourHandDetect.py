import cv2
import numpy as np 

image=cv2.imread('/home/tien/OpenCV/testContour/1 04.jpg')
hsvImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

lower_SkinHSV = np.array([38, 86, 0])
upper_SkinHSV = np.array([121, 255, 255])
mask = cv2.inRange(hsvImage, lower_SkinHSV, upper_SkinHSV)

_, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

#for contour in contours:
lowerHandArea = 100
upperHandArea = 500

for contour in contours:
    area = cv2.contourArea(contour)

    if (area > lowerHandArea) and (area < upperHandArea):
        cv2.drawContours (image, contour, -1, (0, 255, 0), 3)


cv2.imshow('Original Image', image)
cv2.imshow('Mask', mask)

key = cv2.waitKey(0)
cv2.destroyAllWindows()
#learn the HSV & HandArea threshold