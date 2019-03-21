import os
#from os.path import join
import glob
import cv2
import numpy as np 
import matplotlib.pyplot as plt
import time

import json, codecs

from statistics import mean
from functions import passedCondition, caculateIOU, caculateRecall, viusualizeResult
startTime = time.time()

errorList = []
dataPropertisesFilePath = '/home/tien/OpenCV/handDetection/availableData/dataPropertisesFile.json'
listIOUFilePath = '/home/tien/OpenCV/handDetection/availableData/listIOUFile.json'
listRecallFilePath = '/home/tien/OpenCV/handDetection/availableData/listRecallFile.json'
errorListFilePath = '/home/tien/OpenCV/handDetection/availableData/errorListFile.json'
conditionType = 1
dataPropertises = []
listIOU = []
listRecall = []
try:
    with open(dataPropertisesFilePath, 'r+') as dataPropertisesFile:
        dataPropertises = json.load(dataPropertisesFile)
    with open(listIOUFilePath, 'r+') as listIOUFile:
        listIOU = json.load(listIOUFile)
    with open(listRecallFilePath, 'r+') as listRecallFile:
        listRecall = json.load(listRecallFile)
    with open(errorListFilePath, 'r+') as errorListFile:
        errorList = json.load(errorListFile)

    print('Got AVAILABLE data')
except:
    print('Data NOT AVAILABLE. Start exploring root data:')
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


    def quickQuitFunction():
        pictureQuantity = 0
        count = 10000
        #start matching png vs jpg
        #myPath as level0Files
        # def myFunc(): #using myFunc to quit multi loops
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
                                
                                pictureQuantity += 1
                                #print(pictureQuantity)

                                try:
                                    imageFromPathPNG = cv2.imread(pathPNG)
                                    imageFromPathJPG = cv2.imread(pathJPG)

                                    #caculate IoU rate ~ precesion rate                        
                                    IOU = caculateIOU(imageFromPathPNG, imageFromPathJPG, frameHeight, frameWidth, conditionType)
                                    listIOU.append(IOU)

                                    #caculate Recall rate ~ sensivity
                                    Recall = caculateRecall(imageFromPathPNG, imageFromPathJPG, frameHeight, frameWidth, conditionType)
                                    listRecall.append(Recall)

                                    # cv2.imshow(viusualizeResult(imageFromPathPNG, imageFromPathJPG, frameHeight, frameWidth, conditionType))

                                    #caculate total number of pics
                                    
                                    count = count - 1
                                    if count == 0:
                                        dataPropertises.append(pictureQuantity)
                                        return

                                except:
                                    errorList.append(pathJPG)
                                    print("Error!")
        dataPropertises.append(pictureQuantity)
        return
    quickQuitFunction()
    # print(listIOU)
    print('Sucessful Compared all matchable pairs PNG-JPG. Intersection Of Union Ratio and Recall Updated! ErrorList (segmented errors) below: ')                        
    print(errorList)

    #SAVE data to FILES!

    dataPropertises.append(frameHeight)
    dataPropertises.append(frameWidth)

    with open(dataPropertisesFilePath, 'w') as dataPropertisesFile:
        json.dump(dataPropertises, dataPropertisesFile)

    with open(listIOUFilePath, 'w') as listIOUFile:
        json.dump(listIOU, listIOUFile)
    
    with open(listRecallFilePath, 'w') as listRecallFile:
        json.dump(listRecall, listRecallFile)

    with open(errorListFilePath, 'w') as errorListFile:
        json.dump(errorList, errorListFile)

    print('Data saved to files')
print('Max IOU = ' , max(listIOU))
print ('Max Recall = ' , max(listRecall))
print ('Mean Recall = ', mean(listRecall))
print("Program executed in %s seconds " %(time.time() - startTime))
