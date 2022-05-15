from ICM import *


CIRCLE_IMAGE = r"shapes_iamges\circle.jpg"
LONG_IMAGE = r"shapes_images\long_1x3.jpg"
QUAD_IMAGE = r"shapes_images\quad.jpg"
TRI_IMAGE = r"shapes_images\tri_255x217.jpg"


MECH_DRAW1 = r"images\test1.1.jpeg"
MECH_DRAW2 = r"images\crptest1.jpeg"


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


if __name__ == "__main__":

    # circle_img = ImageObj(CIRCLE_IMAGE)
    # long_img = ImageObj(LONG_IMAGE)
    # quad_img = ImageObj(QUAD_IMAGE)
    # tri_img = ImageObj(TRI_IMAGE)

    # tri_img.showImage()

    # ic = ImageComparison(tri_img, quad_img)

    # compareUsingImageSubtraction()
    # compareUsingMSE()

    tryImageCropping()
    # testGetShape()
