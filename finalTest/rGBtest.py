import os
#from os.path import join
import glob
import cv2
import numpy as np 
import matplotlib.pyplot as plt
import time

#import json, codecs
import csv
import pandas

from statistics import mean
from rGBOptionalFunctions import passedCondition, caculateIOU, caculateRecall, viusualizeResult
startTime = time.time()

resultFilePath = '/home/tien/OpenCV/finalTest/availableData/resultFile.csv'
dataPropertisesFilePath = '/home/tien/OpenCV/finalTest/availableData/dataPropertisesFile.csv'
errorListFilePath = '/home/tien/OpenCV/finalTest/availableData/errorListFile.csv'

conditionType = 2
dataPropertisesFrame = pandas.DataFrame(columns = ['Frame Height', 'Frame Width', 'Picture Quantity'])
erroDataFrame = pandas.DataFrame(columns=['Original JPG'])
rGBResultDataFrame = pandas.DataFrame(columns = ['Original JPG', 'Binary PNG', 'IoU', 'Recall'])


try:
    rGBResultDataFrame = pandas.read_csv(resultFilePath)
    
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
        errorQuantity = 0
        count = 5000
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
                                    #listIOU.append(IOU)

                                    #caculate Recall rate ~ sensivity
                                    Recall = caculateRecall(imageFromPathPNG, imageFromPathJPG, frameHeight, frameWidth, conditionType)
                                    #listRecall.append(Recall)

                                    # cv2.imshow(viusualizeResult(imageFromPathPNG, imageFromPathJPG, frameHeight, frameWidth, conditionType))

                                    #caculate total number of pics
                                    
                                    #append result to csvResultDataFrame
                                    #rGBResultDataFrame = rGBResultDataFrame.append(['Original JPG' = pathJPG, 'Binary PNG' = pathPNG, 'IoU' = IOU, 'Recall' = Recall])
                                    rGBResultDataFrame.loc[pictureQuantity-1] = [pathJPG, pathPNG, IOU, Recall]
                                    count = count - 1
                                    if count == 0:
                                        dataPropertisesFrame.loc[0] = [frameHeight, frameWidth, pictureQuantity]
                                        return

                                except:
                                    erroDataFrame.loc[errorQuantity] = [pathJPG]
                                    errorQuantity += 1
                                    print("Error!")
        return
    quickQuitFunction()
    # print(listIOU)
    print('Sucessful Compared all matchable pairs PNG-JPG. Intersection Of Union Ratio, Recall and ErroList  Updated!')                        
    #print(errorList)

    #SAVE data to FILES!

    dataPropertisesFrame.to_csv(dataPropertisesFilePath)
    rGBResultDataFrame.to_csv(resultFilePath)
    erroDataFrame.to_csv(errorListFilePath)
    
print(rGBResultDataFrame)
print('Max IOU = ' , max(rGBResultDataFrame['IoU']))
print('Mean IOU= ' , mean(rGBResultDataFrame['IoU']))
print ('Max Recall = ' , max(rGBResultDataFrame['Recall']))
print ('Mean Recall = ', mean(rGBResultDataFrame['Recall']))
print("Program executed in %s seconds " %(time.time() - startTime))
