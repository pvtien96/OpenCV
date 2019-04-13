from getImageSize import getImageSize
from pairJPGvsPNG import pairJPGvsPNG

dataPath = '/home/tien/OpenCV/handDectectionProject/data/SegmentedData'

(frameHeight, frameWidth) = getImageSize(dataPath)
pairing = pairJPGvsPNG(dataPath)