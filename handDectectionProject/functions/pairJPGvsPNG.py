import os
import cv2 
import pandas

'''
input: dataPath
output: 1. JPG Image Path true-paired with PNG Image Path. Save to ./JPGvsPNG.csv
        2. pairingErrorList (can't read...?). Save to ./pairingErrorList.csv
        return True if save successfully, else False.
'''

def pairingJPGvsPNG(dataPath):
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
dataPath = '/home/tien/OpenCV/handDectectionProject/data/SegmentedData'
pairing = pairJPGvsPNG(dataPath)
'''