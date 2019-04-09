import cv2
import numpy as np
import matplotlib.pyplot as plt

def passedCondition(conditionType, h, s, v):
    """
    if conditionType == 1:
        if ((r>g) and (r>b) and (r>95) and (g>40) and (b>20)):
            return True
    """
    if conditionType == 2:
        if ((0 <= h <= 8) or (172 <= h <=179 )) and (60 <= s <= 100) and (80<= v <=101):
            return True
    return False

def skinDetectingBasedOnBGRAreaWHThreshold(image):
    hsvImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_SkinHSV = np.array([0, 52, 75])
    upper_SkinHSV = np.array([15, 133, 108])

    lowerHandArea = 200
    upperHandArea = 1200

    lowerWidth = 10
    upperWidth = 100

    lowerHeight = 10
    upperHeight = 100

    frameHeight = image.shape[0]
    frameWidth  = image.shape[1]
    outImg = np.zeros((frameHeight, frameWidth, 3), np.uint8)
    mask = cv2.inRange(hsvImage, lower_SkinHSV, upper_SkinHSV)

    _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        area = cv2.contourArea(contour)
        if (lowerHandArea < area < upperHandArea):
            x, y, width, height = cv2.boundingRect(contour)
            #check if width and hieght is ok
            if (lowerWidth < width < upperWidth) and (lowerHeight < height < upperHeight):
                for i in range(x, x + width):
                    for j in range(y, y+height):
                        outImg[j,i] = hsvImage[j,i]
        
    return outImg

def caculateIOU(pngImage, jpgImage, frameHeight, frameWidth, conditionType):
    intersectionAmount = 0
    unionAmount = 0
    #pngImage = pngImage[..., ::-1]
    #jpgImage = jpgImage[..., ::-1]
    jpgHSVImage = skinDetectingBasedOnBGRAreaWHThreshold(jpgImage)

    for i in range(frameHeight):
        for j in range(frameWidth):
            h = jpgHSVImage.item(i, j, 0)
            s = jpgHSVImage.item(i, j, 1)
            v = jpgHSVImage.item(i, j, 2)
            if passedCondition(conditionType, h, s, v):
                unionAmount += 1
                if pngImage.item(i, j, 0) == 255:
                    intersectionAmount += 1
            '''
            else:
                if pngImage.item(i, j, 0) == 255:
                    unionAmount += 1
            '''
        # print(intersectionAmount, ' ', unionAmount)
    return intersectionAmount/unionAmount

def caculateRecall(pngImage, jpgImage, frameHeight, frameWidth, conditionType):
    retrievedAmount = 0
    relevantAmount = 0
    #pngImage = pngImage[..., ::-1]
    #jpgImage = jpgImage[..., ::-1]
    jpgHSVImage = skinDetectingBasedOnBGRAreaWHThreshold(jpgImage)
    
    for i in range(frameHeight):
        for j in range(frameWidth):
            h = jpgHSVImage.item(i, j, 0)
            s = jpgHSVImage.item(i, j, 1)
            v = jpgHSVImage.item(i, j, 2)
            if pngImage.item(i, j, 0) == 255:
                relevantAmount += 1
                if passedCondition(conditionType, h, s, v):
                    retrievedAmount += 1
            #if passedCondition(conditionType, r, g, b):
                
    return retrievedAmount/relevantAmount

def viusualizeResult(pngImage, jpgImage, frameHeight, frameWidth, conditionType):
    #pngImage = pngImage[..., ::-1]
    #jpgImage = jpgImage[..., ::-1]
    jpgHSVImage = cv2.cvtColor(jpgImage, cv2.COLOR_BGR2HSV)

    pngImageOutput = np.zeros((frameHeight, frameWidth, 3), np.uint8)

    for i in range(frameHeight):
        for j in range(frameWidth):
            h = jpgHSVImage.item(i, j, 0)
            s = jpgHSVImage.item(i, j, 1)
            v = jpgHSVImage.item(i, j, 2)
            if passedCondition(conditionType, h, s, v):
                pngImageOutput[i, j] = 75
                '''
                pngImageOutput.item(i, j, 0) = 75
                pngImageOutput.item(i, j, 1) = 75
                pngImageOutput.item(i, j, 2) = 75
                '''
                if pngImage.item(i, j, 0) == 255:
                    pngImageOutput [i, j] = 255
    return(pngImageOutput)

"""
#test 1 image
pathPNG = '/home/tien/OpenCV/Skin/Data/SegmentedData/Binh/1/1.1/1 01.png'
pathJPG = '/home/tien/OpenCV/Skin/Data/SegmentedData/Binh/1/1 (3-19-2018 10-18-37 AM)/1 01.jpg'

print(pathJPG)

imageFromPathPNG = cv2.imread(pathPNG)
imageFromPathJPG = cv2.imread(pathJPG)

plt.imshow(viusualizeResult(imageFromPathPNG, imageFromPathJPG, 480, 640, 2))
plt.show()
"""