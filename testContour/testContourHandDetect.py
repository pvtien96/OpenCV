import cv2
import numpy as np 

image=cv2.imread('/home/tien/OpenCV/testContour/1 03.jpg')
hsvImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)


#(73<r and r<108) and (50<g and g<84) and (48<b and b<79)

lower_SkinBGR = np.uint8([[[48, 50, 73]]])
upper_SkinBGR = np.uint8([[[79, 84, 108]]])



lower_SkinHSV = cv2.cvtColor(lower_SkinBGR, cv2.COLOR_BGR2HSV)
upper_SkinHSV = cv2.cvtColor(upper_SkinBGR, cv2.COLOR_BGR2HSV)

"""
lower_SkinHSV = np.array([2, 87, 73])
upper_SkinHSV = np.array([5, 68, 108])
"""
print(lower_SkinHSV, upper_SkinHSV)

mask = cv2.inRange(hsvImage, lower_SkinHSV, upper_SkinHSV)

_, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

#for contour in contours:
lowerHandArea = 0
upperHandArea = 50000

for contour in contours:
    area = cv2.contourArea(contour)

    if (area > lowerHandArea) and (area < upperHandArea):
        cv2.drawContours (image, contour, -1, (0, 255, 0), 3)


cv2.imshow('Original Image', image)
cv2.imshow('HSV Image', hsvImage)
cv2.imshow('Mask', mask)

key = cv2.waitKey(0)
cv2.destroyAllWindows()
#learn the HSV & HandArea threshold