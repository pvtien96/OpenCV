import cv2
import numpy as np 
from matplotlib import pyplot as plt 

def skinDetectingBasedOnHSVAndAreaThreshold(image):
    #img = img[..., ::-1]
    hsvImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_SkinHSV = np.array([0, 52, 75])
    upper_SkinHSV = np.array([15, 133, 108])

    mask = cv2.inRange(hsvImage, lower_SkinHSV, upper_SkinHSV)

    _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    lowerHandArea = 400
    upperHandArea = 2000

    for contour in contours:
        area = cv2.contourArea(contour)

        if (lowerHandArea < area < upperHandArea):
            cv2.drawContours(image, contour, -1, (0, 255, 0), 3)
            #draw straight bounding rectangle
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(image, (x,y), (x+w, y+h), (0,0,255),2)

            #draw rotated rectangle
            rectangle = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rectangle)
            box = np.int0(box)
            cv2.drawContours(image, [box], 0, (255,0,0), 2)    
    return image

#video = cv2.VideoCapture('/home/tien/OpenCV/testContour/videoTest.avi')
video = cv2.VideoCapture('/home/tien/OpenCV/testContour/5.avi')
if (video.isOpened() == False):
    print("Erro opening video stream or file")
else:
    frameWidth  = video.get(3)
    frameHeight = video.get(4)
    
frameWidth = int(frameWidth)
frameHeight = int(frameHeight)
print(frameWidth, frameHeight)


# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
fourcc = cv2.VideoWriter_fourcc(*'XVID')
outVideo = cv2.VideoWriter('/home/tien/OpenCV/testContour/contourDrawedVideo5.avi', fourcc, 20.0, (frameWidth, frameHeight))

while (video.isOpened()):
    ret, frame = video.read()
    if ret == True:
        contourDrawedImage = skinDetectingBasedOnHSVAndAreaThreshold(frame)
        outVideo.write(contourDrawedImage)

        cv2.imshow('contourDrawedImage', contourDrawedImage)

        """
        #plot show to analyze the hsv parametres
        plt.imshow(contourDrawedImage)
        plt.show()
        """
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
    else:
        break

video.release()
outVideo.release()
cv2.destroyAllWindows()
