import cv2
import sys

imagePath = '/home/tien/OpenCV/faceDetecting/abba.png'
cascPath = "/home/tien/OpenCV/faceDetecting/haarcascade_frontalface_default.xml"

#create the haar cascade
faceCascade = cv2.CascadeClassifier(cascPath)

image = cv2.imread(imagePath)
# cv2.imshow('test image', image)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

"""
cv2.imshow('gray test', gray)
cv2.waitKey(0)
cv2.destroyAllWindows
"""

#detect faces in the image
faces = faceCascade.detectMultiScale(
    gray,
    scaleFactor = 1.1,
    minNeighbors = 5,
    minSize = (30, 30),
    flags = cv2.CASCADE_SCALE_IMAGE
)

print("Found {0} faces".format(len(faces)))

#Draw a rectangle around the faces
for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

cv2.imshow("Faces found", image)
cv2.waitKey(0)