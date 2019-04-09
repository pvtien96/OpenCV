import cv2
import numpy as np 
from matplotlib import pyplot as plt 

def skinDetectingBasedOnBGRAreaWHThreshold(image):
    
    lower_SkinBGR = np.array([48, 50, 73])
    upper_SkinBGR = np.array([79, 84, 108])

    mask = cv2.inRange(image, lower_SkinBGR, upper_SkinBGR)

    _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    lowerHandArea = 200
    upperHandArea = 1200

    lowerWidth = 20
    upperWidth = 70

    lowerHeight = 20
    upperHeight = 70

    for contour in contours:
        area = cv2.contourArea(contour)

        if (lowerHandArea < area < upperHandArea):
            
            #draw straight bounding rectangle
            x, y, width, height = cv2.boundingRect(contour)

            #check if width and hieght is ok
            if (lowerWidth < width < upperWidth) and (lowerHeight < height < upperHeight):
                cv2.drawContours(image, contour, -1, (0, 255, 0), 3)
                cv2.rectangle(image, (x,y), (x+width, y+height), (0,0,255),2)

                #draw rotated rectangle
                rectangle = cv2.minAreaRect(contour)
                box = cv2.boxPoints(rectangle)
                box = np.int0(box)
                cv2.drawContours(image, [box], 0, (255,0,0), 2)    
            
    return image

#video = cv2.VideoCapture('/home/tien/OpenCV/testContour/videoTest.avi')
video = cv2.VideoCapture('/home/tien/OpenCV/testContour/videoTest.avi')
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
outVideo = cv2.VideoWriter('/home/tien/OpenCV/testContour/videoTestBGROut.avi', fourcc, 20.0, (frameWidth, frameHeight))

while (video.isOpened()):
    ret, frame = video.read()
    if ret == True:
        contourDrawnImage = skinDetectingBasedOnBGRAreaWHThreshold(frame)
        outVideo.write(contourDrawnImage)

        cv2.imshow('contourDrawnImage', contourDrawnImage)

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
