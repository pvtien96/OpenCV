import os
#from os.path import join
import glob
import cv2
import numpy as np 
import matplotlib.pyplot as plt
import time

startTime = time.time()
"""
def skinDetecting(img, frameHeight, frameWidth):
    img = img[..., ::-1]

    outImg = np.zeros((frameHeight, frameWidth, 3), np.uint8)
    for i in range(frameHeight):
        for j in range(frameWidth):
            r = img.item(i, j, 0)
            g = img.item(i, j, 1)
            b = img.item(i, j, 2)
            if ((r>g) and (r>b) and (r>95) and (g>40) and (b>20)):
                outImg[i, j] = img[i, j]
                    
    return outImg
"""
rSkinAmount = np.zeros((256,), dtype=int)
gSkinAmount = np.zeros((256,), dtype=int)
bSkinAmount = np.zeros((256,), dtype=int)
#print(rSkinAmount)

rNotSkinAmount = np.zeros((256,), dtype=int)
gNotSkinAmount = np.zeros((256,), dtype=int)
bNotSkinAmount = np.zeros((256,), dtype=int)

def rGBAmountUpdate(img, frameHeight, frameWidth):
    img = img[..., ::-1]

    #outImg = np.zeros((frameHeight, frameWidth, 3), np.uint8)
    for i in range(frameHeight):
        for j in range(frameWidth):
            r = img.item(i, j, 0)
            g = img.item(i, j, 1)
            b = img.item(i, j, 2)
            if ((r>g) and (r>b) and (r>95) and (g>40) and (b>20)):
                #outImg[i, j] = img[i, j]
                #print(r)
                rSkinAmount[r] += 1
                gSkinAmount[g] += 1
                bSkinAmount[b] += 1
            else:
                rNotSkinAmount[r] += 1
                gNotSkinAmount[g] += 1
                bNotSkinAmount[b] += 1
    return 0

"""
myPath = '/home/tien/TestProject/Skin/2(3-30-20184-00-20PM)/*.*'
dirArr = glob.glob(myPath)
#print(dirArr)
print(len(dirArr))
img = cv2.imread(dirArr[0])
frameHeight = img.shape[0]
frameWidth  = img.shape[1]
for i in range(len(dirArr)):
    img = cv2.imread(dirArr[i])
    rGBAmountUpdate(img, frameHeight, frameWidth)
    
    ""
    cv2.imshow(dirArr[i], img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    ""
"""

# myPath = "./Data/"
myPath = "/home/tien/OpenCV/Skin/Data/SegmentedData"
#myPath = "/home/tien/TestProject/Data/SegmentedData"

print(myPath)
'''
for root, directories, filenames in os.walk(myPath):
    if filenames:
        
        imgPath = os.path.join(root, filenames[0])
        # print(imgPath)
        # img = cv2.imread(imgPath)
        # frameHeight = img.shape[0]
        # frameWidth  = img.shape[1]
        break
'''
print('Got frameSize')
files = os.listdir(myPath)
print(files)
for f in files:
    myNewPath = os.path.join(myPath, f)
    # print (myNewPath)
    fileOfUser = os.listdir(myNewPath)
    for fOU in fileOfUser:
        myUserPath = os.path.join(myNewPath, fOU)
        # print(myUserPath)
        lastPath = os.listdir(myUserPath)
        # print(lastPath)
        for i in lastPath:
            if len(i) > 3:
                continue
            for j in lastPath:
                if len(j) > 3 and i[0] == j[0]:
                    pngFinalPath = os.path.join(myUserPath, i)
                    jpgFinalPath = os.path.join(myUserPath, j)
                    # print(pngFinalPath, " ", jpgFinalPath)
                    pngImages = os.listdir(pngFinalPath)
                    jpgImages = os.listdir(jpgFinalPath)
                    for jpgImage in jpgImages:
                        xxx = jpgImage.split('.')[0]+'.png'
                        pantjpg = os.path.join(jpgFinalPath, jpgImage)
                        pantpng = os.path.join(pngFinalPath, xxx)
                        print(pantjpg, " ", pantpng)
                         
'''for root, directories, filenames in os. walk(myPath):
    myPath = myPath + root
'''
'''
for root, directories, filenames in os.walk(myPath):
    print('Working with '+root)
    for filename in filenames:
        if filename.endswith(".jpg"):
            imgPath = os.path.join(root, filename)
            # print(imgPath)
            # img = cv2.imread(imgPath)
            # rGBAmountUpdate(img, frameHeight, frameWidth)
'''
# print(filenames)
'''
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
#plt.xlabel('Pixel Value')
#plt.ylabel('Amount')
plt.plot(gSkinAmount, 'g', gNotSkinAmount, 'k')
#plt.show()

#blue skin plot
plt.subplot(133)
plt.title('Blue Amount Plot')
#plt.xlabel('Pixel Value')
#plt.ylabel('Amount')
plt.plot(bSkinAmount, 'b', bNotSkinAmount, 'k')

print("Program executed in %s seconds " %(time.time() - startTime))
plt.show()
'''