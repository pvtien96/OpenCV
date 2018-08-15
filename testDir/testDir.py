"""
import os
from os.path import join
import glob
import cv2
myPath = '/home/tien/TestProject/Skin/2(3-30-20184-00-20PM)'

"""
"""
#using listdir
dirArr = os.listdir(myPath)
#print(dirArr)
print(len(dirArr))
for i in range (len(dirArr)):
    result = join(myPath, dirArr[i])
    print(result)
    img = cv2.imread(result)
    #cv2.imshow('result', result)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
"""

"""
#using glob
myPath = '/home/tien/TestProject/Skin/2(3-30-20184-00-20PM)/*.*'
dirArr = glob.glob(myPath)
#print(dirArr)
print(len(dirArr))
for i in range(len(dirArr)):
    img = cv2.imread(dirArr[i])
    cv2.imshow(dirArr[i], img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
"""
"""
import pathlib.path
p = Path('.')
"""

"""
import os
import glob
myPath = '/home/Desktop/abc'
dirArr = glob.glob(myPath)
print(dirArr)
subfolders = [f.path for f in os.scandir(myPath) if f.is_dir()]
"""

"""
import os

print("root prints out directories only from what you specified")
print("dirs prints out sub-directories from root")
print("files prints out all files from root and directories")
print("*" * 20)

for root, dirs, files in os.walk("./Desktop/abc"):
    print(root)
    print(dirs)
    print(files)
"""

"""
from os import walk
path = "./Desktop/abc/"
for (dirpath, dirnames, filenames) in walk(path):
    print(dirnames)
    break
"""

"""
#ok listed all file
import os
for root, dirs, files in os.walk("./Desktop/abc"):
    for filename in files:
        #if filename = '*.jpg':
            print(os.path.join(root, filename))
"""
#try to list all .jpg file from dirpath
import os
import time
startTime = time.time()

"""
for root, directories, filenames in os.walk("/home/tien/Desktop"):
    for filename in filenames:
        if filename.endswith(".jpg"):
            print(os.path.join(root, filename))
#print(root)
#print(directories)
#print(filenames)
"""

"""
for root, directories, filenames in os.walk("/home/tien/Desktop/Data"):
    #if filenames:

        #print(filenames[0])
        
        #break
        print(root)
        print(directories)
        print(filenames)
"""

jpgFilenameList = []
pngFilenameList = []

for root, directories, filenames in os.walk("/home/tien/Desktop/Data"):
    for filename in filenames:
        if filename.endswith(".jpg"):
            jpgFilenameList.append(os.path.join(root, filename))
        else:
            if filename.endswith(".png"):
                pngFilenameList.append(os.path.join(root, filename))
                

print(jpgFilenameList.__len__())
print(pngFilenameList.__len__())
jpgFilenameList.sort()
pngFilenameList.sort()
for i in range(100):
    print(jpgFilenameList[i])

for i in range(100):
    print(pngFilenameList[i])

print("--- %s seconds ---" % (time.time() - startTime))