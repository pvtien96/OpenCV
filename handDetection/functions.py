import numpy as np
def passedCondition(conditionType, r, g, b):
    if conditionType == 1:
        if ((r>g) and (r>b) and (r>95) and (g>40) and (b>20)):
            return True
    if conditionType == 2:
        if (73<r and r<108) and (50<g and g<84) and (48<b and b<79):
            return True
    return False

def caculateIOU(pngImage, jpgImage, frameHeight, frameWidth, conditionType):
    intersectionAmount = 0
    unionAmount = 0
    pngImage = pngImage[..., ::-1]
    jpgImage = jpgImage[..., ::-1]

    for i in range(frameHeight):
        for j in range(frameWidth):
            r = jpgImage.item(i, j, 0)
            g = jpgImage.item(i, j, 1)
            b = jpgImage.item(i, j, 2)
            if passedCondition(conditionType, r, g, b):
                unionAmount += 1
                if pngImage.item(i, j, 0) == 255:
                    intersectionAmount += 1
            else:
                if pngImage.item(i, j, 0) == 255:
                    unionAmount += 1
        # print(intersectionAmount, ' ', unionAmount)
    return intersectionAmount/unionAmount

def caculateRecall(pngImage, jpgImage, frameHeight, frameWidth, conditionType):
    retrievedAmount = 0
    relevantAmount = 0
    pngImage = pngImage[..., ::-1]
    jpgImage = jpgImage[..., ::-1]
    
    for i in range(frameHeight):
        for j in range(frameWidth):
            r = jpgImage.item(i, j, 0)
            g = jpgImage.item(i, j, 1)
            b = jpgImage.item(i, j, 2)
            if pngImage.item(i, j, 0) == 255:
                relevantAmount += 1
                if passedCondition(conditionType, r, g, b):
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
