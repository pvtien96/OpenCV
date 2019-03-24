import cv2
import numpy as np 
import matplotlib.pyplot as plt

image=cv2.imread('/home/tien/OpenCV/Skin/Data/SegmentedData/Binh/1/1.1/1 01.png')

im2, contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

lowerHandArea = 500
upperHandArea = 700

print(contours)

for contour in contours:
    area = cv2.contourArea(contour)

    if (lowerHandArea < area < upperHandArea):
        cv2.drawContours (image, contour, -1, (0, 255, 0), 3)


cv2.imshow('Original Image', image)
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