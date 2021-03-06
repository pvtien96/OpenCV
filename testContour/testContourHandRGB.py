import cv2
import numpy as np 
import matplotlib.pyplot as plt

image=cv2.imread('/home/tien/OpenCV/testContour/1 03.jpg')
hsvImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)


#(73<r and r<108) and (50<g and g<84) and (48<b and b<79)

'''
lower_SkinHSV = np.array([0, 52, 75])
upper_SkinHSV = np.array([15, 133, 108])
'''

lower_SkinBGR = np.array([48, 50, 73])
upper_SkinBGR = np.array([79, 84, 108])

print(lower_SkinBGR, upper_SkinBGR)

mask = cv2.inRange(image, lower_SkinBGR, upper_SkinBGR)

_, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

#for contour in contours:
lowerHandArea = 400
upperHandArea = 1000

lowerWidth = 20
upperWidth = 70

lowerHeight = 20
upperHeight = 70


print(contours)

frameHeight = image.shape[0]
frameWidth  = image.shape[1]
outImg = np.zeros((frameHeight, frameWidth, 3), np.uint8)


for contour in contours:
    area = cv2.contourArea(contour)

    if (lowerHandArea < area < upperHandArea):
        x, y, width, height = cv2.boundingRect(contour)
        #check if width and hieght is ok
        if (lowerWidth < width < upperWidth) and (lowerHeight < height < upperHeight):
                for i in range(x, x + width):
                    for j in range(y, y+height):
                        outImg[j,i] = image[j,i]

                cv2.drawContours (image, contour, -1, (0, 255, 0), 3)
                cv2.rectangle(image, (x,y), (x+width, y+height), (0,0,255),2)
                #draw rotated rectangle
                rectangle = cv2.minAreaRect(contour)
                box = cv2.boxPoints(rectangle)
                box = np.int0(box)
                cv2.drawContours(image, [box], 0, (255,0,0), 2)
                #save outImage
                
'''
mask = cv2.inRange(image, lower_SkinBGR, upper_SkinBGR)

_, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
for contour in contours:
        area = cv2.contourArea(contour)
        if (lowerHandArea < area < upperHandArea):
            x, y, width, height = cv2.boundingRect(contour)
            #check if width and hieght is ok
            if (lowerWidth < width < upperWidth) and (lowerHeight < height < upperHeight):
                for i in range(x, x + width):
                    for j in range(y, y+height):
                        outImg[j,i] = image[j,i]

'''
cv2.imshow('Original Image', image)
#cv2.imshow('HSV Image', hsvImage)
cv2.imshow('Mask', mask)
cv2.imshow('outImage', outImg)
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