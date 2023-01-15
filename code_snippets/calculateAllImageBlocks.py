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
