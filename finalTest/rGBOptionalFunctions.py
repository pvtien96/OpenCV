import cv2
import numpy as np
def passedCondition(conditionType, b, g, r):
    if conditionType == 1:
        if ((r>g) and (r>b) and (r>95) and (g>40) and (b>20)):
            return True
    if conditionType == 2:
        if (48<b and b<79) and (50<g and g<84) and (73<r and r<108):
            return True
    return False

def skinDetectingBasedOnBGRAreaWHThreshold(image):
    lower_SkinBGR = np.array([48, 50, 73])
    upper_SkinBGR = np.array([79, 84, 108])

    lowerHandArea = 200
    upperHandArea = 1200

    lowerWidth = 10
    upperWidth = 100

    lowerHeight = 10
    upperHeight = 100

    frameHeight = image.shape[0]
    frameWidth  = image.shape[1]
    outImg = np.zeros((frameHeight, frameWidth, 3), np.uint8)
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
        
    return outImg

def caculateIOU(pngImage, jpgImage, frameHeight, frameWidth, conditionType):
    intersectionAmount = 0
    unionAmount = 0

    jpgThresoldImage = skinDetectingBasedOnBGRAreaWHThreshold(jpgImage)

    for i in range(frameHeight):
        for j in range(frameWidth):
            b = jpgThresoldImage.item(i, j, 0)
            g = jpgThresoldImage.item(i, j, 1)
            r = jpgThresoldImage.item(i, j, 2)
            if passedCondition(conditionType, b, g, r):
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
    jpgThresoldImage = skinDetectingBasedOnBGRAreaWHThreshold(jpgImage)
    for i in range(frameHeight):
        for j in range(frameWidth):
            b = jpgThresoldImage.item(i, j, 0)
            g = jpgThresoldImage.item(i, j, 1)
            r = jpgThresoldImage.item(i, j, 2)
            if pngImage.item(i, j, 0) == 255:
                relevantAmount += 1
                if passedCondition(conditionType, b, g, r):
                    retrievedAmount += 1
            #if passedCondition(conditionType, r, g, b):
                
    return retrievedAmount/relevantAmount

def viusualizeResult(pngImage, jpgImage, frameHeight, frameWidth, conditionType):
    pngImage = pngImage[..., ::-1]
    jpgImage = jpgImage[..., ::-1]

    pngImageOutput = np.zeros((frameHeight, frameWidth, 3), np.uint8)

    for i in range(frameHeight):
        for j in range(frameWidth):
            r = jpgImage.item(i, j, 0)
            g = jpgImage.item(i, j, 1)
            b = jpgImage.item(i, j, 2)
            if passedCondition(conditionType, r, g, b):
                pngImageOutput[i, j] = 75
                '''
                pngImageOutput.item(i, j, 0) = 75
                pngImageOutput.item(i, j, 1) = 75
                pngImageOutput.item(i, j, 2) = 75
                '''
                if pngImage.item(i, j, 0) == 255:
                    pngImageOutput [i, j] = 150
    return(pngImageOutput)
