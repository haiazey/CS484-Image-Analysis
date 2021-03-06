import numpy as np
import cv2
import sys
import scipy.misc
from PIL import Image
from scipy import ndimage

#path of the images
backgroundPath = r'highway/in000470.jpg'
path1 = r'highway/in000550.jpg'
path2 = r'highway/in000750.jpg'
path3 = r'highway/in000850.jpg'

#path of the images
pbPath= r'pedestrians/in000300.jpg'
ppath1 = r'pedestrians/in000356.jpg'
ppath2 = r'pedestrians/in000475.jpg'
ppath3 = r'pedestrians/in000575.jpg'


#***********************************************
#		INITIALIZE
#*******************************************
img = cv2.imread( backgroundPath,0)
img2 = cv2.imread( path1,0)
img3 = cv2.imread( path2,0)
img4 = cv2.imread( path3,0)

# get dimensions of image
width = img.shape[0]
height = img.shape[1]

result1 = cv2.subtract( img4, img)
#cv2.imshow("result1", result1)
cv2.imwrite("result1.png", result1)

result2 = cv2.subtract( img3, img)
#cv2.imshow("result2", result2)
cv2.imwrite("result2.png", result2)

result3 = cv2.subtract( img2, img)
#cv2.imshow("result3", result3)
cv2.imwrite("result3.png", result3)


pimg = cv2.imread( pbPath,0)
pimg2 = cv2.imread( ppath1,0)
pimg3 = cv2.imread( ppath2,0)
pimg4 = cv2.imread( ppath3,0)

presult1 = cv2.subtract( pimg4, pimg)
#cv2.imshow("presult1", presult1)
cv2.imwrite("presult1.png", presult1)

presult2 = cv2.subtract( pimg3, pimg)
#cv2.imshow("presult2", presult2)
cv2.imwrite("presult2.png", presult2)

presult3 = cv2.subtract( pimg2, pimg)
#cv2.imshow("presult3", presult3)
cv2.imwrite("presult3.png", presult3)

 
countd = 0
counte = 0
count = 0
###########################################333
# 			DILATION FROM 1ST PART
#############################################3
def dilation( source_image, struct_el, originRow, originCol):
	global countd
	countd = countd +1
	#number of rows and columns of the struct_el
	numrows = len(struct_el)    
	numcols = len(struct_el[0])  
	#result array for image
	resultImage = np.zeros((width,height))
	#resultImage = np.logical_not(resultImage).astype(int)
	#trace all the pixels
	for i in range (width):
		for j in range (height):
			if( source_image[i][j] == 1) : # if seas black pixel
				if( (i> originRow and j> originCol and i< width-originRow and j <height-originCol)): #check boundaries
					orShape = np.bitwise_or(source_image[ (i-originRow):(i+numrows-originRow), (j-originCol):(j+numcols-originCol) ], struct_el) #anding the pixels 
					for x in range(numrows):
						for y in range( numcols):
							resultImage[i-originRow+x][j-originCol+y] = orShape[x][y]# changing the pixels
	#change pixel to create binary image
	for i in range (width):
		for j in range (height):
		
			if( resultImage[i][j] == 1) :
				 resultImage[i][j] = 255
	#cv2.imshow("Binary Image2",source_image)
	#from array to binary
	img2 = Image.fromarray(resultImage.astype('uint8'))
	img2.save('dilation%i.png' % countd)
	img2.show()
	return img2,resultImage
###########################################################3
#				EROSION FROM 1ST PART
###########################################################3333
def erosion( source_image, struct_el, originRow, originCol):
	global counte
	counte = counte +1
	#most part are same as dilation but only not and operator or operator
	numrows = len(struct_el)   
	numcols = len(struct_el[0]) 
	resultImage2 = np.zeros((width,height))
	#resultImage2 = np.logical_not(resultImage2).astype(int)
	for i in range (width):
		for j in range (height):
			if( source_image[i][j] == 1) :
				if( (i> originRow and j> originCol and i< width-originRow and j <height-originCol)): #check boundaries
					orShape = np.bitwise_and(source_image[ (i-originRow):(i+numrows-originRow), (j-originCol):(j+numcols-originCol) ], struct_el)
					if( np.array_equal( orShape , struct_el)):
						resultImage2[i][j] = 1# changing the pixels

	for i in range (width):
		for j in range (height):
			if( resultImage2[i][j] == 1) :
				 resultImage2[i][j] = 255
	#cv2.imshow("Binary Image2",source_image)
	
	img3 = Image.fromarray(resultImage2.astype('uint8'))
	img3.save('erosion%i.png' %counte)
	img3.show()
	return img3,resultImage2
##############################################3333
#                 labeling
#########################################3

def color_components(labels):
	global count
	count = count + 1
	# Map component labels to hue val
	label_hue = np.uint8(179*labels/np.max(labels))
	blank_ch = 255*np.ones_like(label_hue)
	labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])

	# cvt to BGR for display
	labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)

	# set bg label to black
	labeled_img[label_hue==0] = 0

	cv2.imshow('labeled%i.png'%count, labeled_img)
	cv2.imwrite('labeled%i.png'%count, labeled_img)
	cv2.waitKey()

	
######################################3333
#		REMOVE NOISE
############################################
# thresholding

ret, bw_img = cv2.threshold(result1,0,255,cv2.THRESH_BINARY_INV)
threshold = 0.2
new_indice = np.where(bw_img/255>=threshold, 1, 0)

struct_element = [[0,1,0],[1,1,1],[0,1,0]]
struct_element3 = [[1,1,1],[1,1,1],[1,1,1]]
struct_element4 = [[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1]]
struct_element5 =[[1,1,1,1,1,1,1],[1,1,1,1,1,1,1],[1,1,1,1,1,1,1],[1,1,1,1,1,1,1],[1,1,1,1,1,1,1],[1,1,1,1,1,1,1],[1,1,1,1,1,1,1]]
originrow = 1
origincol = 1
originrow2 = 2
origincol2 = 2

originrow3 = 3
origincol3 = 3
e_img, e_result = erosion(new_indice, struct_element4, originrow2, origincol2)
e_img = cv2.imread( 'erosion%i.png'%counte,0)
ret, bw_img = cv2.threshold(e_img,0,255,cv2.THRESH_BINARY)
ero = np.where(bw_img/255>=threshold, 1, 0)
dimg, dresult = dilation(ero, struct_element4, originrow2, origincol2)

###############################################3333
ret, bw_img = cv2.threshold(result2,0,255,cv2.THRESH_BINARY_INV)
new_indice = np.where(bw_img/255>=threshold, 1, 0)
e_img, e_result = erosion(new_indice, struct_element4, originrow2, origincol2)
e_img = cv2.imread( 'erosion%i.png'%counte,0)
ret, bw_img = cv2.threshold(e_img,0,255,cv2.THRESH_BINARY)
ero = np.where(bw_img/255>=threshold, 1, 0)
dimg, dresult = dilation(ero, struct_element4, originrow2, origincol2)

###############################################3333
ret, bw_img = cv2.threshold(result3,50,255,cv2.THRESH_BINARY)
new_indice = np.where(bw_img/255>=threshold, 1, 0)
e_img, e_result = erosion(new_indice, struct_element, originrow2, origincol2)
e_img = cv2.imread( 'erosion%i.png'%counte,0)
ret, bw_img = cv2.threshold(e_img,0,255,cv2.THRESH_BINARY)
ero = np.where(bw_img/255>=threshold, 1, 0)
dimg, dresult = dilation(ero, struct_element4, originrow2, origincol2)
###############################################3333
ret, bw_img = cv2.threshold(presult1,0,255,cv2.THRESH_BINARY)
#bw_img = np.invert(bw_img)
#cv2.imshow("th", bw_img)
new_indice = np.where(bw_img/255>=threshold, 0, 1)
e_img, e_result = erosion(new_indice, struct_element4, originrow2, origincol2)
e_img = cv2.imread( 'erosion%i.png'%counte,0)
ret, bw_img = cv2.threshold(e_img,0,255,cv2.THRESH_BINARY)
ero = np.where(bw_img/255>=threshold, 1, 0)
dimg, dresult = erosion(ero, struct_element, originrow, origincol)

###############################################3333
ret, bw_img = cv2.threshold(presult2,10,255,cv2.THRESH_BINARY)
cv2.imshow("th", bw_img)
new_indice = np.where(bw_img/255>=threshold, 1, 0)
e_img, e_result = erosion(new_indice, struct_element, originrow2, origincol2)
e_img = cv2.imread( 'erosion%i.png'%counte,0)
ret, bw_img = cv2.threshold(e_img,0,255,cv2.THRESH_BINARY)
ero = np.where(bw_img/255>=threshold, 1, 0)
dimg, dresult = dilation(ero, struct_element4, originrow2, origincol2)
###############################################3333
ret, bw_img = cv2.threshold(presult3,10,255,cv2.THRESH_BINARY)
cv2.imshow("th", bw_img)
new_indice = np.where(bw_img/255>=threshold, 1, 0)
e_img, e_result = erosion(new_indice, struct_element, originrow2, origincol2)
e_img = cv2.imread( 'erosion%i.png'%counte,0)
ret, bw_img = cv2.threshold(e_img,0,255,cv2.THRESH_BINARY)
ero = np.where(bw_img/255>=threshold, 1, 0)
dimg, dresult = dilation(ero, struct_element4, originrow2, origincol2)
#####################################333333

img = cv2.imread('dilation1.png', 0)
img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)[1]  
ret, labels = cv2.connectedComponents(img)
color_components(labels)


img = cv2.imread('dilation2.png', 0)
img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)[1]  
ret, labels = cv2.connectedComponents(img)
color_components(labels)

img = cv2.imread('dilation3.png', 0)
img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)[1]  
ret, labels = cv2.connectedComponents(img)
color_components(labels)

img = cv2.imread('dilation4.png', 0)
img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)[1]  
ret, labels = cv2.connectedComponents(img)
color_components(labels)

img = cv2.imread('dilation5.png', 0)
img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)[1]  
ret, labels = cv2.connectedComponents(img)
color_components(labels)

img = cv2.imread('erosion5.png', 0)
img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)[1]  
ret, labels = cv2.connectedComponents(img)
color_components(labels)
cv2.waitKey(0)
cv2.destroyAllWindows()
