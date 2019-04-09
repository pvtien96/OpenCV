import cv2
import numpy as np 
import matplotlib.pyplot as plt

#image=cv2.imread('/home/tien/OpenCV/testContour/1 03.jpg')
image = cv2.imread('/home/tien/OpenCV/Skin/Data/SegmentedData/Hung/2/4 (3-23-2018 1-44-41 PM)/4 11.jpg')
hsvImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)


#(73<r and r<108) and (50<g and g<84) and (48<b and b<79)

"""
#get available BGR and convert to HSV. Failed!
lower_SkinBGR = np.uint8([[[0, 60, 80]]])
upper_SkinBGR = np.uint8([[[8, 100, 101]]])

lower_SkinHSV = cv2.cvtColor(lower_SkinBGR, cv2.COLOR_BGR2HSV)
upper_SkinHSV = cv2.cvtColor(upper_SkinBGR, cv2.COLOR_BGR2HSV)
"""


lower_SkinHSV = np.array([0, 52, 75])
upper_SkinHSV = np.array([15, 133, 108])


"""
lower_SkinHSV = np.array([0, 0, 0])
upper_SkinHSV = np.array([100, 100, 100])
"""

print(lower_SkinHSV, upper_SkinHSV)

mask = cv2.inRange(hsvImage, lower_SkinHSV, upper_SkinHSV)

_, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

#for contour in contours:
lowerHandArea = 600
upperHandArea = 1000

print(contours)

for contour in contours:
    area = cv2.contourArea(contour)

    if (lowerHandArea < area < upperHandArea):
        cv2.drawContours (image, contour, -1, (0, 255, 0), 3)

        #draw straight bounding rectangle
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(image, (x,y), (x+w, y+h), (0,0,255),2)

        #draw rotated rectangle
        rectangle = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rectangle)
        box = np.int0(box)
        cv2.drawContours(image, [box], 0, (255,0,0), 2)


cv2.imshow('Original Image', image)
cv2.imshow('HSV Image', hsvImage)
cv2.imshow('Mask', mask)
key = cv2.waitKey(0)
cv2.destroyAllWindows()

"""
plt.subplot(131)
plt.title('Original Image')
plt.imshow(image)

plt.subplot(132)
plt.title('hSVImage')
plt.imshow(hsvImage)

plt.subplot(133)
plt.title('Mask')
plt.imshow(mask)

plt.show()
"""

#learn the HSV & HandArea threshold