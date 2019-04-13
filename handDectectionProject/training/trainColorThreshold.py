from functions import *

dataPath = '/home/tien/OpenCV/handDectectionProject/data/SegmentedData'
errorListFilePath = '/home/tien/OpenCV/handDetectionProject/training/errorListFile.csv'
errorDataFrame = pandas.DataFrame(columns=['Original JPG'])
#(frameHeight, frameWidth) = getImageSize(dataPath)

#pairJPGvsPNG = pairJPGvsPNG(dataPath)
colorSpace = 'bGR'
(xSkinAmount, ySkinAmount, zSkinAmount, xNotSkinAmount, yNotSkinAmount, zNotSkinAmount) = initXYZAmount(colorSpace)

JPGvsPNGFilePath = '/home/tien/OpenCV/handDectectionProject/functions/JPGvsPNG.csv'
JPGvsPNGDataFrame = pandas.read_csv(JPGvsPNGFilePath)
pictureQuantity = len(JPGvsPNGDataFrame['JPG Path'])
errorQuantity = 0
for i in range(pictureQuantity):
    pathJPG = JPGvsPNGDataFrame['JPG Path'][i]
    pathPNG = JPGvsPNGDataFrame['PNG Path'][i]
    print("Working with: ", pathJPG, " and ", pathPNG)                            
    try:
        imageFromPathPNG = cv2.imread(pathPNG)
        imageFromPathJPG = cv2.imread(pathJPG)                        
        xYZAmountUpdateByComparing2Images(imageFromPathPNG, imageFromPathJPG, xSkinAmount, ySkinAmount, zSkinAmount, xNotSkinAmount, yNotSkinAmount, zNotSkinAmount, colorSpace)                                    
    except:
        errorDataFrame.loc[errorQuantity] = [pathJPG]
        errorQuantity += 1
        print("Error!")
saveData(xSkinAmount, ySkinAmount, zSkinAmount, xNotSkinAmount, yNotSkinAmount, zNotSkinAmount, colorSpace)
showChart(xSkinAmount, ySkinAmount, zSkinAmount, xNotSkinAmount, yNotSkinAmount, zNotSkinAmount, colorSpace)