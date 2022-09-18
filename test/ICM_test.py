import sys

sys.path.insert(0, "../../imageComparison")

from ICM import *

MAINFILE = ""
COMPAREFILE = ""

# CIRCLE_IMAGE = r"shapes_iamges\circle.jpg"
# LONG_IMAGE = r"shapes_images\long_1x3.jpg"
# QUAD_IMAGE = r"shapes_images\quad.jpg"
# TRI_IMAGE = r"shapes_images\tri_255x217.jpg"


MECH_DRAW1 = r"images\test1.1.jpeg"
MECH_DRAW2 = r"images\crptest1.jpeg"
MECH_DRAW3 = r"images\images.png"


# TEST_FILE = r"images\test1.jpg"
# COMPARE_FILE = r"images\test1c.jpg"


# DIFFERENT_COMPARE_FILE = r"images\images.png"
# DIFFERENT_TEST_FILE_1 = r"images\test1.1.jpeg"
# DIFFERENT_TEST_FILE_2 = r"images\test1.2.jpeg"

DIFFIMAGE = r"images\diff_image1.jpg"


def compareUsingImageSubtraction():

    ic.ImageSubtraction()


def compareUsingMSE():
    ic.MeanSquareError()


def tryImageCropping():
    img = ImageObj(MECH_DRAW1)
    img.cropImage()


def testGetShape():

    img = ImageObj(MECH_DRAW1)
    img.getShape()
    print(img.shape)


def testCropImage2():
    img = ImageObj(MECH_DRAW3)
    img.cropImage()


def testImageComparison(img1, img2):
    if CHECK_IMAGE_FILES:
        checkFile()

    image1 = ImageObj(img1)

    # image2 = ImageObj(DIFFERENT_TEST_FILE_2)
    image2 = ImageObj(img2)

    image1.showImage()
    image2.showImage()

    # IMAGE SUBTRACTION TESTING

    ic = ImageComparison(image1, image2)
    ic.ImageSubtraction(save_fig=True)

    # MSE TESTING

    print("MEAN SQUARE ERROR : ", ic.MeanSquareError())


def testImageObjthreshold():
    img = ImageObj(DIFFIMAGE)
    img.checkNegetiveThreshold(50)


if __name__ == "__main__":

    # circle_img = ImageObj(CIRCLE_IMAGE)
    # long_img = ImageObj(LONG_IMAGE)
    # quad_img = ImageObj(QUAD_IMAGE)
    # tri_img = ImageObj(TRI_IMAGE)

    # tri_img.showImage()

    # ic = ImageComparison(tri_img, quad_img)

    # compareUsingImageSubtraction()
    # compareUsingMSE()

    # tryImageCropping()
    # testCropImage2()
    # testGetShape()

    MAINFILE = r""

    testImageComparison()

    # testImageObjthreshold()
