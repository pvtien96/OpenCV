import cv2
import numpy as np 
import matplotlib.pyplot as plt

hSkinAmount = np.zeros((180,), dtype=int)
sSkinAmount = np.zeros((256,), dtype=int)
vSkinAmount = np.zeros((256,), dtype=int)

hNotSkinAmount = np.zeros((1000,), dtype=int)
sNotSkinAmount = np.zeros((256,), dtype=int)
vNotSkinAmount = np.zeros((256,), dtype=int)


def hSVAmountUpdateByComparing2Images(pngImage, jpgImage, frameHeight, frameWidth):
    #pngImage = pngImage[..., ::-1]
    jpgHSVImage = cv2.cvtColor(jpgImage, cv2.COLOR_BGR2HSV)

    for i in range(frameHeight):
        for j in range(frameWidth):
            h = jpgHSVImage.item(i, j, 0)
            s = jpgHSVImage.item(i, j, 1)
            v = jpgHSVImage.item(i, j, 2)
            if pngImage.item(i, j, 0) == 255:
                hSkinAmount[h] += 1
                sSkinAmount[s] += 1
                vSkinAmount[v] += 1
            else:
                hNotSkinAmount[h] += 1
                sNotSkinAmount[s] += 1
                vNotSkinAmount[v] += 1
    return 0

pathPNG = '/home/tien/OpenCV/Skin/Data/SegmentedData/Binh/1/1.1/1 01.png'
pathJPG = '/home/tien/OpenCV/Skin/Data/SegmentedData/Binh/1/1 (3-19-2018 10-18-37 AM)/1 01.jpg'

print(pathJPG)

imageFromPathPNG = cv2.imread(pathPNG)
imageFromPathJPG = cv2.imread(pathJPG)

#imageFromPathJPG = imageFromPathJPG[..., ::-1]
plt.imshow(imageFromPathJPG)
plt.show()
plt.imshow(imageFromPathPNG)
plt.show()

hSVAmountUpdateByComparing2Images(imageFromPathPNG, imageFromPathJPG, 480, 640)

print(hSkinAmount)
print(hNotSkinAmount)
