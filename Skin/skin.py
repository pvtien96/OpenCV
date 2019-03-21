import numpy as np 
import cv2
import matplotlib.pyplot as plt 


img = cv2.imread('/home/tien/OpenCV/Skin/1 04.jpg')
img = img[..., ::-1]

NRow = img.shape[0]
NCol = img.shape[1]

outImg = np.zeros((NRow, NCol, 3), np.uint8)
plt.subplot(121)
plt.imshow(outImg)

for i in range(NRow):
    for j in range(NCol):
        r = img.item(i, j, 0)
        g = img.item(i, j, 1)
        b = img.item(i, j, 2)
        if ((r>g) and (r>b) and (r>95) and (g>40) and (b>20)):
            outImg[i, j] = img[i, j]
plt.subplot(122)
plt.imshow(outImg)
plt.show()

'''
imgPath = '/home/tien/OpenCV/Skin/2.1.png'
img = cv2.imread(imgPath)
img = img[..., ::-1]
plt.subplot(121)
plt.imshow(img)
# plt.show()

plt.subplot(122)
plt.imshow(img)
plt.show()
NRow = img.shape[0]
NCol = img.shape[1]

sum = 0

for i in range(NRow):
    for j in range(NCol):
        r = img.item(i, j, 0)
        g = img.item(i, j, 1)
        b = img.item(i, j, 2)
        if r == 255 :
            sum += 1
            print (r, " ", g, " ", b , " ", i)
print(sum/(NRow*NCol))
'''