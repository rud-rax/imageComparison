from ICM import *
import matplotlib.pyplot as plt
import numpy as np
import cv2

CIRCLE_IMAGE = r"shapes_iamges\circle.jpg"
LONG_IMAGE = r"shapes_images\long_1x3.jpg"
QUAD_IMAGE = r"shapes_images\quad.jpg"
TRI_IMAGE = r"shapes_images\tri_255x217.jpg"


MECH_DRAW1 = r"images\test1.1.jpeg"
MECH_DRAW2 = r"images\crptest1.jpeg"
MECH_DRAW3 = r"images\images.png"


TEST_FILE = r"images\test1.jpg"
COMPARE_FILE = r"images\test1c.jpg"
DIFFERENT_COMPARE_FILE = r"images\images.png"
DIFFERENT_TEST_FILE_1 = r"images\test1.1.jpeg"
DIFFERENT_TEST_FILE_2 = r"images\test1.2.jpeg"

DIFFIMAGE = r"images\diff_image1.jpg"


def testImageObjthreshold():
    img = ImageObj(DIFFIMAGE)
    img.checkNegetiveThreshold(50)


def testImageComparison():
    if CHECK_IMAGE_FILES:
        checkFile()

    image1 = ImageObj(TEST_FILE)

    image2 = ImageObj(DIFFERENT_TEST_FILE_2)

    image1.showImage()
    image2.showImage()

    # IMAGE SUBTRACTION TESTING

    ic = ImageComparison(image1, image2)
    ic.ImageSubtraction(save_fig=True)

    # MSE TESTING

    print("MEAN SQUARE ERROR : ", ic.MeanSquareError())


if __name__ == "__main__":

    testImageComparison()
