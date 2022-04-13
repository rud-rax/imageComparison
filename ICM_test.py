from ICM import *


CIRCLE_IMAGE = r"shapes/circle.jpg"
LONG_IMAGE = r"shapes/long_1x3.jpg"
QUAD_IMAGE = r"quad.jpg"
TRI_IMAGE = r"shapes/tri_255x217.jpg"


def compareUsingImageSubtraction():

    ic.ImageSubtraction()


def compareUsingMSE():
    ic.MeanSquareError()


if __name__ == "__main__":

    circle_img = ImageObj(CIRCLE_IMAGE)
    long_img = ImageObj(LONG_IMAGE)
    quad_img = ImageObj(QUAD_IMAGE)
    tri_img = ImageObj(TRI_IMAGE)

    ic = ImageComparison(circle_img, long_img)

    compareUsingImageSubtraction()
    # compareUsingMSE()
