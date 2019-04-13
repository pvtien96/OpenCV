import os
import cv2

#pick an typical random image to get image's frame size; 1 time only for all others
def getImageSize(dataPath):
    for root, __, filenames in os.walk(dataPath):
        if filenames:
            imagePath = os.path.join(root, filenames[0])
            image = cv2.imread(imagePath)
            frameHeight = image.shape[0]
            frameWidth  = image.shape[1]
        break
    print('Got frameSize', frameHeight, frameWidth)
    return (frameHeight, frameWidth)