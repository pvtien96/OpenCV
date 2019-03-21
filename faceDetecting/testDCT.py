import cv2
import cv2 as cv
import numpy as np   

img1 = cv2.imread('/home/tien/OpenCV/faceDetecting/abba.png')
# or use cv2.CV_LOAD_IMAGE_GRAYSCALE 
img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
cv2.imshow('input', img1)
w,h = img1.shape
# make a 32bit float for doing the dct within
img2 = np.zeros((w,h), dtype=np.float32)
print (img1.shape, img2.shape)
img2 = img2+img1[:w, :h]
dct1 = cv2.dct(img2)
key = -1
while(key < 0):
    cv2.imshow("DCT", dct1)
    key = cv2.waitKey(1)
cv2.destroyAllWindows()

