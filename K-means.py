import numpy as np
import matplotlib.pyplot as ply
import cv2
import random
import struct




"""imgOld = cv2.imread("/Users/sisirreddy/Desktop/Development/Python/ML/Assignment2/IconsLandVistaSportIconsDemo/PNG/16x16/Basketball_Ball.png")
img = np.array(imgOld,dtype=np.int)
#cv2.imshow("img",img)
print("Hey")
img[0:10,0:10] = [0,0,255]
blank_image = np.zeros((16,16,3), np.uint8)
img = np.array(img,dtype=np.uint8)
blank_image = img
#img = np.array(imgOld,dtype=np.uint8)
#print(img)
cv2.imshow("Img",blank_image)
cv2.waitKey(0)"""




def generateRandomNums(k,imgShape):  #generating random points from the image to start clustering
	pointIndex = []
	for i in range(0,k):
		x = random.randint(0,imgShape[0]-1)
		y = random.randint(0,imgShape[1]-1)
		if(len(pointIndex)!=0):
			flag=0
			for row in pointIndex:
				if row[0]==x and row[1]==y:
					flag =1
			if flag==1:
				while flag!=0:
					x = random.randint(0,imgShape[0])
					y = random.randint(0,imgShape[1])
					flag2=0
					for row in pointIndex:
						if row[0]==x and row[1]==y:
							flag2 =1
					if flag2==0:
						flag=0
			pointIndex.append([x,y])
		else:
			pointIndex.append([x,y])
	return pointIndex



def findDist(currentPoint,point):# gives euclidean distance between 2 points
	sqrDist=0
	for i in range(0,len(point)):
		dist = abs(currentPoint[i]-point[i])
		sqrDist+= dist**2
	euclideanDist = sqrDist**0.5
	return euclideanDist


def modifyPoints(clusterIndex,points,img): # the points are chnaged according to the cluster they belong to
	k=0
	for cluster in clusterIndex:
		sumArr=[]
		for point in cluster:
			RGB=img[point[0]][point[1]]

			if(len(sumArr)==0):
				sumArr.append(RGB[0])
				sumArr.append(RGB[1])
				sumArr.append(RGB[2])

			else:
				sumArr[0] =sumArr[0]+RGB[0]
				sumArr[1] =sumArr[1]+RGB[1]
				sumArr[2] =sumArr[2]+RGB[2]
				
				
		for i in range(0,len(sumArr)):
			sumArr[i]=sumArr[i]/len(cluster)
		points[k] = sumArr
		k+=1
	return points





imgOld = cv2.imread("./Images/Beach.jpg")

imgOld = cv2.resize(imgOld, (400, 300)) #resizing image to make computration easy

img = np.array(imgOld,dtype=np.int)

k=6 # adjust k values here
print(f"K = {k}")
#cv2.imshow("Real",imgOld)
#print(img.shape)
#print(random.randint(0,16))
pointIndex = generateRandomNums(k,img.shape)
#print(pointIndex)
points=[]
rowCount=0
colCount=0
clusterIndex=[] #a 2d array that maintains the index of points belonging to each cluster
for i in range(0,len(pointIndex)):
	points.append(img[pointIndex[i][0]][pointIndex[i][1]])

for i in range(0,k):
	clusterIndex.append([[0,0]])


for count in range(0,2): # looped 100 times to get the result
	rowCount=0
	colCount=0
	for row in img:
		colCount=0
		for col in row:
			distArr=[]
			for i in range(0,k):
				distArr.append(findDist(col,points[i]))
			minIndex = distArr.index(min(distArr)) # for a given point in image, the distances to all clusters calculatex and the cluster with min distance is chosen and the point's index is placed in that cluster
			clusterIndex[minIndex].append([rowCount,colCount])
			colCount+=1
		rowCount+=1

	for i in range(0,k):
		clusterIndex[i].pop(0)
	points = modifyPoints(clusterIndex,points,img)
	print("Done ",count)

points = np.array(points,dtype=np.uint8)
#print(type(points[0][0]))
clusterCount=0
for cluster in clusterIndex:
	for point in cluster:
		img[point[0]][point[1]] = points[clusterCount]
	clusterCount+=1

img = np.array(img,dtype=np.uint8)

blankImg = np.zeros((img.shape[0],img.shape[1],3),np.uint8)
blankImg = img

cv2.imshow("k = %d"%(k,),blankImg)
cv2.waitKey(0)



		

		
