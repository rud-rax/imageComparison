from ICM import *

image1_file_path = r"industrySample/drw1/drw1o0.jpg"
image2_file_path = r"industrySample/drw1/drw1s0.jpg"

img1 = ImageObj(image1_file_path)
img2 = ImageObj(image2_file_path)
cordinates = testImageBlock2(img1, img2)
# All diff in one image
inOne(cordinates, img1.img, img2.img)