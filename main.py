from ICM import *

img1 = ImageObj(INDUSTRYSAMPLE1)
img2 = ImageObj(INDUSTRYSAMPLE2)
cordinates = testImageBlock2(img1, img2)
# All diff in one image
inOne(cordinates, img1.img, img2.img)