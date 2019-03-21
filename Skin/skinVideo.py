import numpy as np 
import matplotlib.pyplot as plt 
import cv2

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

cap = cv2.VideoCapture('/home/tien/OpenCV/Skin/video.avi')
if (cap.isOpened() == False):
    print("Erro opening video stream or file")
else:
    frameHeight = cap.get(4)
    frameWidth  = cap.get(3)

# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
outVideo = cv2.VideoWriter('outVideo', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (frameWidth, frameHeight))

while (cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        outVideo.write(skinDetecting(frame, frameHeight, frameWidth))        
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
    else:
        break
cap.release()
outVideo.release()
cv2.destroyAllWindows()