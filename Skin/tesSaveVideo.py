
"""
import numpy as np 
import cv2
import matplotlib.pyplot as plt 

cap = cv2.VideoCapture('/home/tien/TestProject/Skin/video.avi')

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

if cap.isOpened() == False:
    print('Erro opening video')
else:
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            #frame = cv2.flip(frame, 0)

            out.write(frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
cap.release()
out.release()
cv2.destroyAllWindows()     
"""

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
    frameHeight = int(cap.get(4))
    frameWidth  = int(cap.get(3))

# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
#10 = fps
outVideo = cv2.VideoWriter('/home/tien/TestProject/Skin/outVideo.avi', fourcc, 10, (frameWidth, frameHeight))

while (cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        #outVideo.write(frame)
        outVideo.write(skinDetecting(frame, frameHeight, frameWidth))        
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
    else:
        break
cap.release()
outVideo.release()
cv2.destroyAllWindows()