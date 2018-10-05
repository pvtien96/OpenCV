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

print(myPath)

#pick an typical random image to get image's frame size; 1 time only for all others
for root, directories, filenames in os.walk(myPath):
    if filenames:
        
        imgPath = os.path.join(root, filenames[0])
        print(imgPath)
        img = cv2.imread(imgPath)
        frameHeight = img.shape[0]
        frameWidth  = img.shape[1]
        break
print('Got frameSize')

#start matching png vs jpg
files = os.listdir(myPath)
print(files)
for f in files:
    myNewPath = os.path.join(myPath, f)
    # print (myNewPath)
    fileOfUser = os.listdir(myNewPath) #Binh Hung Hoang
    for fOU in fileOfUser:
        myUserPath = os.path.join(myNewPath, fOU)
        # print(myUserPath)
        lastPath = os.listdir(myUserPath)
        # print(lastPath)
        
        for i in lastPath:
            if len(i) > 4:
                continue
            for j in lastPath:
                if len(j) > 4 and i.split('.')[0] == j.split(' ')[0] :
                    pngFinalPath = os.path.join(myUserPath, i)
                    jpgFinalPath = os.path.join(myUserPath, j)
                    # print(pngFinalPath, " ", jpgFinalPath)
                    pngImages = os.listdir(pngFinalPath)
                    jpgImages = os.listdir(jpgFinalPath)
                    for jpgImage in jpgImages:
                        xxx = jpgImage.split('.')[0]+'.png'
                        pathJPG = os.path.join(jpgFinalPath, jpgImage)
                        pathPNG = os.path.join(pngFinalPath, xxx)
                        print("Working with: ", pathJPG, " and ", pathPNG)
                        try:
                        
                            imageFromPathPNG = cv2.imread(pathPNG)
                            imageFromPathJPG = cv2.imread(pathJPG)                        
                            rGBAmountUpdateByComparing2Images(imageFromPathPNG, imageFromPathJPG, frameHeight, frameWidth)
                        except:
                            errorList.append(pathJPG)

#red skin plot
plt.subplot(131)
plt.title('Red Amount Plot')
plt.xlabel('Pixel Value')
plt.ylabel('Amount')
plt.plot(rSkinAmount, 'r', rNotSkinAmount, 'k')
#plt.show()

#green skin plot
plt.subplot(132)
plt.title('Green Amount Plot')
plt.xlabel('Pixel Value')
plt.ylabel('Amount')
plt.plot(gSkinAmount, 'g', gNotSkinAmount, 'k')
#plt.show()

#blue skin plot
plt.subplot(133)
plt.title('Blue Amount Plot')
plt.xlabel('Pixel Value')
plt.ylabel('Amount')
plt.plot(bSkinAmount, 'b', bNotSkinAmount, 'k')

plt.show()

print("Program executed in %s seconds " %(time.time() - startTime))