import os
#from os.path import join
import glob
import cv2
import numpy as np 
import matplotlib.pyplot as plt
import time

from sklearn import preprocessing
import json, codecs

startTime = time.time()

rSkinAmount = np.zeros((256,), dtype=int)
gSkinAmount = np.zeros((256,), dtype=int)
bSkinAmount = np.zeros((256,), dtype=int)

#print(rSkinAmount[255])

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
print('Got frameSize', frameHeight, frameWidth)

#start matching png vs jpg
#myPath as level0Files
def myFunc(): #using myFunc to quit multi loops
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
                                return
                            except:
                                errorList.append(pathJPG)
                                print("Error!")
    return
myFunc()
print('Sucessful Compared all matchable pairs PNG-JPG. Amount Updated! ErrorList (segmented errors) below: ')                        
print(errorList)

# try to standardlize the data manually
maxValueOfRSkinAmount = max(rSkinAmount)
maxValueOfGSkinAmount = max(gSkinAmount)
maxValueOfBSkinAmount = max(bSkinAmount)

standardlizedRSkinAmount = np.zeros((256,))
standardlizedGSkinAmount = np.zeros((256,))
standardlizedBSkinAmount = np.zeros((256,))


for i in range(256):
    standardlizedRSkinAmount[i] = rSkinAmount[i] / maxValueOfRSkinAmount
    standardlizedGSkinAmount[i] = gSkinAmount[i] / maxValueOfGSkinAmount
    standardlizedBSkinAmount[i] = bSkinAmount[i] / maxValueOfBSkinAmount

maxValueOfRNotSkinAmount = max(rNotSkinAmount)
maxValueOfGNotSkinAmount = max(gNotSkinAmount)
maxValueOfBNotSkinAmount = max(bNotSkinAmount)

standardlizedRNotSkinAmount = np.zeros((256,))
standardlizedGNotSkinAmount = np.zeros((256,))
standardlizedBNotSkinAmount = np.zeros((256,))

for i in range(256):
    standardlizedRNotSkinAmount[i] = rNotSkinAmount[i] / maxValueOfRNotSkinAmount
    standardlizedGNotSkinAmount[i] = gNotSkinAmount[i] / maxValueOfGNotSkinAmount
    standardlizedBNotSkinAmount[i] = bNotSkinAmount[i] / maxValueOfBNotSkinAmount

#process data, optional!

fixRNotSkinAmount = rNotSkinAmount
fixGNotSkinAmount = gNotSkinAmount
fixBNotSkinAmount = bNotSkinAmount

fixRNotSkinAmount[255] = fixRNotSkinAmount[254]
fixGNotSkinAmount[255] = fixGNotSkinAmount[254]
fixBNotSkinAmount[255] = fixBNotSkinAmount[254]

maxValueOfFixRNotSkinAmount = max(fixRNotSkinAmount)
maxValueOfFixGNotSkinAmount = max(fixGNotSkinAmount)
maxValueOfFixBNotSkinAmount = max(fixBNotSkinAmount)

standardlizedFixRNotSkinAmount = np.zeros((256,))
standardlizedFixGNotSkinAmount = np.zeros((256,))
standardlizedFixBNotSkinAmount = np.zeros((256,))

for i in range(256):
    standardlizedFixRNotSkinAmount[i] = fixRNotSkinAmount[i] / maxValueOfFixRNotSkinAmount
    standardlizedFixGNotSkinAmount[i] = fixGNotSkinAmount[i] / maxValueOfFixGNotSkinAmount
    standardlizedFixBNotSkinAmount[i] = fixBNotSkinAmount[i] / maxValueOfFixBNotSkinAmount

"""
#using preprocessing library #NOT UNDERSTOOD!
reshapedRSkinAmount = rSkinAmount.reshape(-1, 1)
normalizedRSkinAmount = preprocessing.normalize(reshapedRSkinAmount)
print (normalizedRSkinAmount)
"""

#red skin plot
plt.subplot(431)
plt.title('Red Amount Plot')
# plt.xlabel('Pixel Value')
plt.ylabel('Amount')
plt.plot (rSkinAmount, 'r')

#green skin plot
plt.subplot(432)
plt.title('Green Amount Plot')
# plt.xlabel('Pixel Value')
plt.ylabel('Amount')
plt.plot (gSkinAmount, 'g')

#blue skin plot
plt.subplot(433)
plt.title('Blue Amount Plot')
# plt.xlabel('Pixel Value')
plt.ylabel('Amount')
plt.plot (bSkinAmount, 'b')

#red vs non-red skin plot
plt.subplot(434)
plt.title('Red vs Non-Red Amount Plot')
# plt.xlabel('Pixel Value')
plt.ylabel('Amount')
plt.plot(rSkinAmount, 'r', rNotSkinAmount, 'k')
#plt.show()

#green vs non-green skin plot
plt.subplot(435)
plt.title('Green vs Non-Green Amount Plot')
# plt.xlabel('Pixel Value')
plt.ylabel('Amount')
plt.plot(gSkinAmount, 'g', gNotSkinAmount, 'k')
#plt.show()

#blue vs non-blue skin plot
plt.subplot(436)
plt.title('Blue vs Non-Blue Amount Plot')
# plt.xlabel('Pixel Value')
plt.ylabel('Amount')
plt.plot(bSkinAmount, 'b', bNotSkinAmount, 'k')

#Standardlized Amount plot

#standardlized: red vs non-red skin plot
plt.subplot(437)
plt.title('Standardlized red vs non-red')
plt.plot(standardlizedGSkinAmount, 'r', standardlizedRNotSkinAmount, 'k')

#standardlized: green vs non-green skin plot
plt.subplot(438)
plt.title('Standardlized green vs non-green')
plt.plot(standardlizedGSkinAmount, 'g', standardlizedGNotSkinAmount, 'k')

#standardlized: blue vs non-blue skin plot
plt.subplot(439)
plt.title('Standardlized blue vs non-blue')
plt.plot(standardlizedBSkinAmount, 'b', standardlizedBNotSkinAmount, 'k')

#standardlized fixed: red vs non-red skin plot
plt.subplot(4, 3, 10)
plt.title('Fixed Standardlized red vs non-red')
plt.plot(standardlizedRSkinAmount, 'r', standardlizedFixRNotSkinAmount, 'k')

#standardlized fixed: green vs non-green skin plot
plt.subplot(4, 3, 11)
plt.title('Fixed Standardlized green vs non-green')
plt.plot(standardlizedGSkinAmount, 'g', standardlizedFixGNotSkinAmount, 'k')

#standardlized fixed: blue vs non-blue skin plot
plt.subplot(4, 3, 12)
plt.title('Fixed Standardlized blue vs non-blue')
plt.plot(standardlizedBSkinAmount, 'b', standardlizedFixBNotSkinAmount, 'k')

#process data with FILES!
toListRSkinAmount = rSkinAmount.tolist()
toListGSkinAmount = gSkinAmount.tolist()
toListBSkinAmount = bSkinAmount.tolist()
rSkinAmountFile = '/home/tien/OpenCV/skinStatistic/groundTruthData/rSkinAmount.json'
gSkinAmountFile = '/home/tien/OpenCV/skinStatistic/groundTruthData/gSkinAmount.json'
bSkinAmountFile = '/home/tien/OpenCV/skinStatistic/groundTruthData/bSkinAmount.json'
toListRNotSkinAmount = rNotSkinAmount.tolist()
toListGNotSkinAmount = gNotSkinAmount.tolist()
toListBNotSkinAmount = bNotSkinAmount.tolist()
rNotSkinAmountFile = '/home/tien/OpenCV/skinStatistic/groundTruthData/rNotSkinAmount.json'
gNotSkinAmountFile = '/home/tien/OpenCV/skinStatistic/groundTruthData/gNotSkinAmount.json'
bNotSkinAmountFile = '/home/tien/OpenCV/skinStatistic/groundTruthData/bNotSkinAmount.json'

#below line save data in .json format JSONIFY 
json.dump(toListRSkinAmount, codecs.open(rSkinAmountFile, 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)
json.dump(toListGSkinAmount, codecs.open(gSkinAmountFile, 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)
json.dump(toListBSkinAmount, codecs.open(bSkinAmountFile, 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)
json.dump(toListRNotSkinAmount, codecs.open(rNotSkinAmountFile, 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)
json.dump(toListGNotSkinAmount, codecs.open(gNotSkinAmountFile, 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)
json.dump(toListBNotSkinAmount, codecs.open(bNotSkinAmountFile, 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)

#UNJSONIFY

rSkinAmountText = codecs.open(rSkinAmountFile, 'r', encoding='utf-8').read()
toListRSkinAmount = json.loads(rSkinAmountText)
rSkinAmount = np.array(toListRSkinAmount)
print(rSkinAmount)


print("Program executed in %s seconds " %(time.time() - startTime))

plt.show()