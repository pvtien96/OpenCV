def passedConditon(conditionType, r, g, b):
    if conditionType == 1:
        if ((r>g) and (r>b) and (r>95) and (g>40) and (b>20)):
            return True
    if conditionType == 2:
        if (73<r and r<108) and (50<r and r<84) and (48<b and b<79):
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
            if passedConditon(conditionType, r, g, b):
                unionAmount += 1
                if pngImage.item(i, j, 0) == 255:
                    intersectionAmount += 1
            else:
                if pngImage.item(i, j, 0) == 255:
                    unionAmount += 1
                
    return intersectionAmount/unionAmount