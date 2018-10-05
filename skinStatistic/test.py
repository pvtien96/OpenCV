import os
#from os.path import join
import glob
import cv2
import numpy as np 
import matplotlib.pyplot as plt
import time

startTime = time.time()

rSkinAmount = np.zeros((256,), dtype=int)
gSkinAmount = np.zeros((256,), dtype=int)
bSkinAmount = np.zeros((256,), dtype=int)
#print(rSkinAmount)

rNotSkinAmount = np.zeros((256,), dtype=int)
gNotSkinAmount = np.zeros((256,), dtype=int)
bNotSkinAmount = np.zeros((256,), dtype=int)

errorList = []

def rGBAmountUpdateByComparing2Images(pngImage, jpgImage, frameHeight, frameWidth):
    pngImage = pngImage[..., ::-1]
    jpgImage = jpgImage[..., ::-1]

    for i in range(frameHeight):
        for j in range(frameWidth):
            r = jpgImage.item(i, j, 0)
            g = jpgImage.item(i, j, 1)
            b = jpgImage.item(i, j, 2)
            if pngImage.item(i, j, 0) == 255:
                rSkinAmount[r] += 1
                gSkinAmount[g] += 1
                bSkinAmount[b] += 1
            else:
                rNotSkinAmount[r] += 1
                gNotSkinAmount[g] += 1
                bNotSkinAmount[b] += 1
    return 0

myPath = "/home/tien/OpenCV/Skin/Data/SegmentedData"

#print(myPath)

#pick an typical random image to get image's frame size; 1 time only for all others
for root, directories, filenames in os.walk(myPath):
    if filenames:
        
        imgPath = os.path.join(root, filenames[0])
        #print(imgPath)
        img = cv2.imread(imgPath)
        frameHeight = img.shape[0]
        frameWidth  = img.shape[1]
        break
print('Got frameSize')

#start matching png vs jpg
#myPath as level0Files

level1Files = os.listdir(myPath)  #level1Files = ['Binh', 'Hung', 'Hoang']
# print(level1Files)
for level1File in level1Files: 
    level1FilesPath = os.path.join(myPath, level1File)
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
                    pngImages = os.listdir(pngFinalPath)
                    jpgImages = os.listdir(jpgFinalPath)
                    for jpgImage in jpgImages:
                        matchedIndex = jpgImage.split('.')[0]+'.png' # matchedIndex = 3 11.pgn
                        #print(matchedIndex)
                        pathJPG = os.path.join(jpgFinalPath, jpgImage)
                        pathPNG = os.path.join(pngFinalPath, matchedIndex)
                        print("Working with: ", pathJPG, " and ", pathPNG)
                        
                        try:
                            imageFromPathPNG = cv2.imread(pathPNG)
                            imageFromPathJPG = cv2.imread(pathJPG)                        
                            rGBAmountUpdateByComparing2Images(imageFromPathPNG, imageFromPathJPG, frameHeight, frameWidth)
                        except:
                            errorList.append(pathJPG)

print('Sucessful Compared all matchable pairs PNG-JPG. Amount Updated! ErrorList (segmented errors) below: ')                        
print(errorList)

#red skin plot
plt.subplot(231)
plt.title('Red Amount Plot')
plt.xlabel('Pixel Value')
plt.ylabel('Amount')
plt.plot (rSkinAmount, 'r')

#green skin plot
plt.subplot(232)
plt.title('Green Amount Plot')
plt.xlabel('Pixel Value')
plt.ylabel('Amount')
plt.plot (gSkinAmount, 'g')

#blue skin plot
plt.subplot(233)
plt.title('Blue Amount Plot')
plt.xlabel('Pixel Value')
plt.ylabel('Amount')
plt.plot (bSkinAmount, 'b')

#red vs non-red skin plot
plt.subplot(234)
plt.title('Red vs Non-Red Amount Plot')
plt.xlabel('Pixel Value')
plt.ylabel('Amount')
plt.plot(rSkinAmount, 'r', rNotSkinAmount, 'k')
#plt.show()

#green vs non-green skin plot
plt.subplot(235)
plt.title('Green vs Non-Green Amount Plot')
plt.xlabel('Pixel Value')
plt.ylabel('Amount')
plt.plot(gSkinAmount, 'g', gNotSkinAmount, 'k')
#plt.show()

#blue vs non-blue skin plot
plt.subplot(236)
plt.title('Blue vs Non-Blue Amount Plot')
plt.xlabel('Pixel Value')
plt.ylabel('Amount')
plt.plot(bSkinAmount, 'b', bNotSkinAmount, 'k')

#print(rSkinAmount)
print("Program executed in %s seconds " %(time.time() - startTime))

plt.show()

