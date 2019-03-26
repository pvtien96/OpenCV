import cv2
import numpy as np 

def skinDetectingBasedOnHSVAndAreaThreshold(image):
    #img = img[..., ::-1]
    hsvImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_SkinHSV = np.array([0, 52, 75])
    upper_SkinHSV = np.array([15, 133, 108])

    mask = cv2.inRange(hsvImage, lower_SkinHSV, upper_SkinHSV)

    _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    lowerHandArea = 600
    upperHandArea = 1000

    for contour in contours:
        area = cv2.contourArea(contour)

        if (lowerHandArea < area < upperHandArea):
            cv2.drawContours(image, contour, -1, (0, 255, 0), 3)
                
    return image

video = cv2.VideoCapture('/home/tien/OpenCV/testContour/videoTest.avi')
if (video.isOpened() == False):
    print("Erro opening video stream or file")
else:
    frameHeight = video.get(4)
    frameWidth  = video.get(3)

print(frameHeight, frameWidth)
"""
# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
outVideo = cv2.VideoWriter('outVideo', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (frameWidth, frameHeight))

while (video.isOpened()):
    ret, frame = video.read()
    if ret == True:
        outVideo.write(skinDetectingBasedOnHSVAndAreaThreshold(frame, frameHeight, frameWidth))        
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
    else:
        break
"""
"""
fourcc = cv2.VideoWriter_fourcc(*'XVID')
outVideo = cv2.VideoWriter('outVideo.avi', fourcc, 20.0, (480, 640))
while (video.isOpened()):
    ret, frame = video.read()
    if ret == True:
        outVideo.write(skinDetectingBasedOnHSVAndAreaThreshold(frame))        
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
    else:
        break

video.release()
outVideo.release()
cv2.destroyAllWindows()
"""