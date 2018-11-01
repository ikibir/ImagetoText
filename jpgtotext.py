import cv2

isim = input("Image Name: ")
img = cv2.imread(isim )
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
i=0
j=0
n=1
file = open("image.txt","w")
while i<len(img):
	while j<len(img[i]):
		if(img[i][j] < 25):
			file.write("0")
		elif(img[i][j] < 50):
			file.write("1")
		elif(img[i][j] < 75):
			file.write("Z")
		elif(img[i][j] < 100):
			file.write("X")
		elif(img[i][j] < 125):
			file.write("+")
		elif(img[i][j] < 150):
			file.write("$")
		elif(img[i][j] < 175):
			file.write("&")
		elif(img[i][j] < 200):
			file.write("*")
		elif(img[i][j] < 220):
			file.write("%")
		else:
			file.write("#")
		j+=n
	file.write("\n")
	j=0
	i+=n
