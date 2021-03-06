'''
 * TakeHome Quiz
 * Zeynep Nur Öztürk
 * 21501472
'''
import cv2
import sys
from matplotlib import pyplot as plt
import numpy as np

# path of the image
path = r'image.jpg'
 
#Resize the image as 1000 pixel
W = 1000.
image = cv2.imread(path)
height, width, depth = image.shape
imgScale = W / width
newX, newY = image.shape[1] * imgScale, image.shape[0] * imgScale
newimg = cv2.resize(image,(int(newX),int(newY)))
cv2.waitKey(0)
cv2.imwrite("resizeimg.jpg",newimg)

# split into channels
channels = cv2.split(newimg)

# tuple to select colors of each channel line
color = ("b", "g", "r") 

# create the histogram plot, with three lines, one for each color

plt.xlim([0, 256])
for(channel, c) in zip(channels, color):
    histogram = cv2.calcHist(
        images = [channel], 
        channels = [0], 
        mask = None, 
        histSize = [256], 
        ranges = [0, 256])

    plt.plot(histogram, color = c)

plt.xlabel("Color value")
plt.ylabel("Pixels")
plt.show()




# Skin color
min_HSV = np.array([0, 58, 30], dtype = "uint8")
max_HSV = np.array([33, 255, 255], dtype = "uint8")

imageHSV = cv2.cvtColor(newimg, cv2.COLOR_BGR2HSV)
cv2.imshow('hsv',imageHSV)

skinRegionHSV = cv2.inRange(imageHSV, min_HSV, max_HSV)
cv2.imshow('ranged',skinRegionHSV)

skinHSV = cv2.bitwise_and(newimg, newimg, mask = skinRegionHSV)
cv2.imshow('skin',skinHSV)
cv2.imwrite("SkinHSV.png", skinHSV)

#RGB_again = cv2.cvtColor(skinHSV, cv2.COLOR_HSV2RGB)
gray = cv2.cvtColor(skinHSV, cv2.COLOR_RGB2GRAY)
cv2.imwrite("SkinGray.png", gray)

ret, bw_img = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
cv2.imshow('binary',bw_img)
cv2.imwrite("SkinBinaryface.png", bw_img)





# Trees

light_green = np.array([35, 0, 0], dtype = "uint8")
dark_green = np.array([90, 255, 255], dtype = "uint8")

imageHSV = cv2.cvtColor(newimg, cv2.COLOR_BGR2HSV)
cv2.imshow('hsv',imageHSV)

greenmask = cv2.inRange(imageHSV, light_green, dark_green)
cv2.imshow('ranged',greenmask)

green = cv2.bitwise_and(newimg, newimg, mask = greenmask)

cv2.imwrite("Trees.png", green)
cv2.imshow('green',green)

# Delete white
lower_white = np.array([0,0,168])
upper_white = np.array([172,111,255])

whitemask = cv2.inRange(imageHSV, lower_white, upper_white)
cv2.imshow('ranged',whitemask)

white = cv2.bitwise_and(newimg, newimg, mask = whitemask)

result = cv2.subtract(green,white)

cv2.imwrite("white.png", white)
cv2.imshow('result',result)
cv2.imwrite("SubtractedTrees.png", result)

gray = cv2.cvtColor(result, cv2.COLOR_RGB2GRAY)

ret, bw_img3 = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
cv2.imshow('binary',bw_img3)
cv2.imwrite("resultTree.png", bw_img3)





# Building 

result1 = cv2.subtract(white, skinHSV)

cv2.imwrite("Building_v1.png", result1)
cv2.imshow('result',white)

# DElete whiteness of face
lwhite = np.array([0,0,250])
uwhite = np.array([255,255,255])

twhitemask = cv2.inRange(imageHSV, lwhite, uwhite)
cv2.imshow('twhitemask',twhitemask)
cv2.imwrite("Building_v2.png", twhitemask)

twhite = cv2.bitwise_and(newimg, newimg, mask = twhitemask)

# Delete road
result2 = cv2.subtract(result1,twhite)
cv2.imshow('twhite',result2)
cv2.imwrite("Building_v3.png", result2)

RGB_again = cv2.cvtColor(green, cv2.COLOR_HSV2RGB)
gray = cv2.cvtColor(RGB_again, cv2.COLOR_RGB2GRAY)

ret, bw_img2 = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
cv2.imshow('binary',bw_img2)
cv2.imwrite("Building_v4.png", bw_img2)


cv2.waitKey(delay = 0)
