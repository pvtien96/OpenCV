import os
import cv2
import pandas
import numpy as np

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
'''
#test
dataPath = '/home/tien/OpenCV/handDectectionProject/data/SegmentedData'
(Height, Width) = getImageSize(dataPath)
'''

'''
input: dataPath
output: 1. JPG Image Path true-paired with PNG Image Path. Save to ./JPGvsPNG.csv
        2. pairingErrorList (can't read...?). Save to ./pairingErrorList.csv
        return True if save successfully, else False.
'''

def pairJPGvsPNG(dataPath):
    JPGvsPNGFilePath = '/home/tien/OpenCV/handDectectionProject/functions/JPGvsPNG.csv'
    pairingErrorListFilePath = '/home/tien/OpenCV/handDetectionProject/functions/pairingErrorList.csv'
    JPGvsPNGDataFrame = pandas.DataFrame(columns = ['JPG Path', 'PNG Path'])
    errorDataFrame = pandas.DataFrame(columns=['JPG Path', 'PNG Path'])
    pictureQuantity = 0
    errorQuantity = 0

    #dataPath as level0Files
    level1Files = os.listdir(dataPath)  #level1Files = ['Binh', 'Hung', 'Hoang']
    # print(level1Files)
    for level1File in level1Files: 
        level1FilesPath = os.path.join(dataPath, level1File)
        # print (level1FilesPath) # level1FilesPath = /home/tien/OpenCV/Skin/Data/SegmentedData/Binh
        level2Files = os.listdir(level1FilesPath) 
        for level2File in level2Files:
            level2FilesPath = os.path.join(level1FilesPath, level2File)
            # print(level2FilesPath) # level2FilesPath = /home/tien/OpenCV/Skin/Data/SegmentedData/Binh/1
            level3Files = os.listdir(level2FilesPath)
            # print(level3Files) # level3Files = ['5 (3-19-2018 10-18-43 AM)', '1 (3-19-2018 10-18-37 AM)', '4.1', '3 (3-19-2018 10-18-39 AM)', '2 (3-19-2018 10-18-38 AM)', '1.1', '2.1', '5.1', '3.1', '4 (3-19-2018 10-18-41 AM)']
            
            for level3FileLabel in level3Files: # level3FileLabel = ['1.1']
                if len(level3FileLabel) > 4:
                    continue
                for level3FileOrigin in level3Files: # level3FileOrigin = ['1 (3-19-2018 10-18-37 AM)']
                    if len(level3FileOrigin) > 4 and level3FileLabel.split('.')[0] == level3FileOrigin.split(' ')[0] :
                        pngFinalPath = os.path.join(level2FilesPath, level3FileLabel)
                        jpgFinalPath = os.path.join(level2FilesPath, level3FileOrigin)
                        # print(pngFinalPath, " ", jpgFinalPath)
                        #pngImages = os.listdir(pngFinalPath) #unecessary
                        jpgImages = os.listdir(jpgFinalPath)
                        for jpgImage in jpgImages:
                            matchedIndex = jpgImage.split('.')[0]+'.png' # matchedIndex = 3 11.pgn
                            #print(matchedIndex)
                            pathJPG = os.path.join(jpgFinalPath, jpgImage)
                            pathPNG = os.path.join(pngFinalPath, matchedIndex)
                            #print("Working with: ", pathJPG, " and ", pathPNG)
                            
                            try:
                                __ = cv2.imread(pathPNG)
                                JPGvsPNGDataFrame.loc[pictureQuantity] = [pathJPG, pathPNG]
                                pictureQuantity += 1
                            except:                                
                                errorDataFrame.loc[errorQuantity] = [pathJPG, pathPNG]
                                errorQuantity += 1
                                print('Error!')
    try:
        JPGvsPNGDataFrame.to_csv(JPGvsPNGFilePath)
        if errorQuantity:
            errorDataFrame.to_csv(pairingErrorListFilePath)
        print('Paired all JPG vs PNG. Returned ./JPGvsPNG.csv and ./pairingErrorList.csv')
        return True
    except:
        print('Error Pairing JPGvsPNG') 
        return False
    return

'''
#init XYZ Skin & Not Skin Amount
#input: colorSpace
'''
def initXYZAmount(colorSpace):
    if colorSpace == 'bGR':
        bSkinAmount = np.zeros((256,), dtype=int)    
        gSkinAmount = np.zeros((256,), dtype=int)
        rSkinAmount = np.zeros((256,), dtype=int)
        bNotSkinAmount = np.zeros((256,), dtype=int)
        gNotSkinAmount = np.zeros((256,), dtype=int)
        rNotSkinAmount = np.zeros((256,), dtype=int)
        return (bSkinAmount, gSkinAmount, rSkinAmount, bNotSkinAmount, gNotSkinAmount, rNotSkinAmount)
    if colorSpace == 'hSV':
        hSkinAmount = np.zeros((180,), dtype=int)
        sSkinAmount = np.zeros((256,), dtype=int)
        vSkinAmount = np.zeros((256,), dtype=int)
        hNotSkinAmount = np.zeros((180,), dtype=int)
        sNotSkinAmount = np.zeros((256,), dtype=int)
        vNotSkinAmount = np.zeros((256,), dtype=int)
        return (hSkinAmount, sSkinAmount, vSkinAmount, hNotSkinAmount, sNotSkinAmount, vNotSkinAmount)
    if colorSpace == 'yCrCb':
        ySkinAmount = np.zeros((256,), dtype=int)        
        CrSkinAmount = np.zeros((256,), dtype=int)
        CbSkinAmount = np.zeros((256,), dtype=int)
        yNotSkinAmount = np.zeros((256,), dtype=int)        
        CrNotSkinAmount = np.zeros((256,), dtype=int)
        CbNotSkinAmount = np.zeros((256,), dtype=int)
        return (ySkinAmount, CrSkinAmount, CbSkinAmount, yNotSkinAmount, CrNotSkinAmount, CbNotSkinAmount)
    return()

'''
#xYZ Skin & Not Skin Amount Update
'''
def xYZAmountUpdateByComparing2Images(pngImage, jpgImage, xSkinAmount, ySkinAmount, zSkinAmount, xNotSkinAmount, yNotSkinAmount, zNotSkinAmount, colorSpace):
    frameHeight = pngImage.shape[0]
    frameWidth  = pngImage.shape[1]
    if colorSpace == 'bGR':
        jpgConvertedImage = jpgImage
    if colorSpace == 'hSV':
        jpgConvertedImage = cv2.cvtColor(jpgImage, cv2.COLOR_BGR2HSV)
    if colorSpace == 'yCrCb':
        jpgConvertedImage = cv2.cvtColor(jpgImage, cv2.COLOR_BGR2YCrCb)
    for i in range(frameHeight):
        for j in range(frameWidth):
            x = jpgConvertedImage.item(i, j, 0)
            y = jpgConvertedImage.item(i, j, 1)
            z = jpgConvertedImage.item(i, j, 2)
            if pngImage.item(i, j, 0) == 255:
                xSkinAmount[x] += 1
                ySkinAmount[y] += 1
                zSkinAmount[z] += 1
            else:
                xNotSkinAmount[x] += 1
                yNotSkinAmount[y] += 1
                zNotSkinAmount[z] += 1
    return (xSkinAmount, ySkinAmount, zSkinAmount, xNotSkinAmount, yNotSkinAmount, zNotSkinAmount)

'''
#
'''
def saveData(xSkinAmount, ySkinAmount, zSkinAmount, xNotSkinAmount, yNotSkinAmount, zNotSkinAmount, colorSpace):

    return True
def showChart(xSkinAmount, ySkinAmount, zSkinAmount, xNotSkinAmount, yNotSkinAmount, zNotSkinAmount, colorSpace):
    
    return True
    

    