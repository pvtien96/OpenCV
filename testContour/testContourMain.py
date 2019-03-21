import numpy as np 
import cv2

im = cv2.imread('/home/tien/OpenCV/testContour/1 04.jpg')
imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(imgray, 127, 255, 0)
im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

"""
cv2.drawContours(im2, contours, -1, (0,255,0), 3)
cv2.imshow('imgContours', im2)
cv2.waitKey(0)
cv2.destroyAllWindows
"""
for contour in contours:
    area = cv2.contourArea(contour)
    if area <10:
        cv2.drawContours(im2, contour, -1, (0, 255, 0), 3)

cv2.imshow('imOriginal', im)
cv2.imshow('imGray', imgray)
cv2.imshow('imContoursPassedArea', im2)

cv2.waitKey(0)
cv2.destroyAllWindows