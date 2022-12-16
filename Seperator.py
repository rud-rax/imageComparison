import cv2 as cv
import numpy as np


class ImageSub2:
    def imageSub(img1, img2):
        pass


INDUSTRYSAMPLE1 = r"industrySample/drawing0.jpg"
INDUSTRYSAMPLE2 = r"industrySample/drawing10.jpg"

# INDUSTRYSAMPLE1 = r"industrySample/1.jpg"
# INDUSTRYSAMPLE2 = r"industrySample/2.jpg"

REDUCTION_SCALE = 2

img1 = cv.imread(INDUSTRYSAMPLE1)
img2 = cv.imread(INDUSTRYSAMPLE2)

img1 = cv.resize(
    img1, (img1.shape[0] // REDUCTION_SCALE, img1.shape[1] // REDUCTION_SCALE)
)
img2 = cv.resize(
    img2, (img2.shape[0] // REDUCTION_SCALE, img2.shape[1] // REDUCTION_SCALE)
)

# cv.imwrite('D/:5.jpg',img1)
diff = cv.absdiff(img1, img2)
grayscale = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)

gray = cv.cvtColor(diff, cv.COLOR_BGR2GRAY)
blurr = cv.GaussianBlur(gray, (5, 5), 0)
_, thresh = cv.threshold(blurr, 10, 255, cv.THRESH_BINARY)
dilated = cv.erode(thresh, None, iterations=3)

# Finding Contour:
contours, _ = cv.findContours(dilated, cv.RETR_CCOMP, cv.CHAIN_APPROX_NONE)
dst = cv.drawContours(img1, contours, -1, (127, 127, 127), 2)

for contour in contours:
    print("p")
    (x, y, w, h) = cv.boundingRect(contour)
    dst = cv.rectangle(img2, (x, y), (x + w, y + h), (0, 255, 0), 2)

print(len(contours))

cv.namedWindow("Image", cv.WINDOW_KEEPRATIO)
cv.imshow("Image", dst)
# cv.imshow("Image1", img1)cv.findContours
# cv.imshow("Image2", img2)

k = cv.waitKey(0)
if k == 27:
    cv.destroyAllWindows()
