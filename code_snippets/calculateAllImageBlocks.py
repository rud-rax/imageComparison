import cv2
import numpy as np
import pandas as pd

FILEPATH = r"industrySample/page0.jpg"

# READ THE IMAGE INTO A VARIABLE
img = cv2.imread(FILEPATH)

# PRINT RESOLUTION OF IMAGE
print(img.shape)

# DISPLAY THE IM""AGE ON THE WINDOW
cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
cv2.imshow("Image", img)

# HALT THE PROGRAM
cv2.waitKey(0)

# CLOSE ALL WINDOWS
cv2.destroyAllWindows()

# CONVERT IMAGE INTO NUMPY ARRAY
imgarray = np.asarray(img)

# print(imgarray)
# df = pd.DataFrame(imgarray)
# print(df.head())

# for shade in imgarray:
#     print(shade)

#     break
# print(len(shade))


# CONVERT NP ARRAY BACK TO IMAGE



# class BlockCoordinates:
#     def __init__(self, p1: list, p2: list):
#         self.x1, self.y1 = p1
#         self.x2, self.y2 = p2
#         # self.type = type


# def calLeftSlope(self):
#     # call for calculating the TopLeft(p1) and BottomRight(p4) coordinates of the image
#     # returns value of p1 and p4 respectively

#     return [[self.x2, self.y1], [self.x1, self.y2]]

# def calRightSlope(self):
#     # call for calculating the TopRight(p2) and BottomLeft(p3) coordinates of the image
#     # returns value of p2 and p3 respectively
#     return [[self.x2, self.y1], [self.x1, self.y2]]