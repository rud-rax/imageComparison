from ICM import *
from pdf2image import convert_from_path
import cv2
import numpy as np

MAINFILE = r"industrySample/sample1.pdf"
COMPAREFILE = ""


img1 = convert_from_path(MAINFILE)
for i in range(len(img1)):
    img1[i].save(f"industrySample/page1{i}.jpg", "JPEG")


IMAGEPATH = r"industrySample/page0.jpg"

# img1 = ImageObj(IMAGEPATH)
# print(img1.checkImage())
# img1.showImage()
# print(img1.getResolution())


# sift = cv2.xfeatures2d.SIFT

# cv2.SIFT_create()
