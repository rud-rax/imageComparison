from ICM import *
import matplotlib.pyplot as plt
import numpy as np
import cv2
import concurrent.futures
import time

# CIRCLE_IMAGE = r"shapes_iamges\circle.jpg"
# LONG_IMAGE = r"shapes_images\long_1x3.jpg"
# QUAD_IMAGE = r"shapes_images\quad.jpg"
# TRI_IMAGE = r"shapes_images\tri_255x217.jpg"


# MECH_DRAW1 = r"images\test1.1.jpeg"
# MECH_DRAW2 = r"images\crptest1.jpeg"
# MECH_DRAW3 = r"images\images.png"


# TEST_FILE = r"images\test1.jpg"
# COMPARE_FILE = r"images\test1c.jpg"
# DIFFERENT_COMPARE_FILE = r"images\images.png"
# DIFFERENT_TEST_FILE_1 = r"images\test1.1.jpeg"
# DIFFERENT_TEST_FILE_2 = r"images\test1.2.jpeg"

DIFFIMAGE = r"images\diff_image1.jpg"

INDUSTRYSAMPLE1 = r"industrySample/page0.jpg"
INDUSTRYSAMPLE2 = r"industrySample/page10.jpg"

# INDUSTRYSAMPLE1 = r"industrySample/1.jpg"
# INDUSTRYSAMPLE2 = r"industrySample/2.jpg"


BLOCKSIZE = 200
MSE_THRESHOLD = 1000


def imageContour(img1, img2):
    diff = cv2.absdiff(img1, img2)
    grayscale = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blurr = cv2.GaussianBlur(gray, (3, 3), 0)
    _, thresh = cv2.threshold(blurr, 10, 255, cv2.THRESH_BINARY)
    dilated = cv2.erode(thresh, None, iterations=3)

    # Finding Contour:
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    dst = cv2.drawContours(img1, contours, -1, (127, 127, 127), 2)

    for contour in contours:
        # print("p")
        (x, y, w, h) = cv2.boundingRect(contour)
        if cv2.contourArea(contour) < 100:
            continue
        dst = cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 0, 255), 2)

    print("Image Resolution = ", img1.shape)
    cv2.imshow("DST", dst)
    return x, y, w, h


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


def testImageResolution():

    # sam1path = INDUSTRYSAMPLE1
    # sam2path = INDUSTRYSAMPLE2

    # create image objects
    image1 = ImageObj(INDUSTRYSAMPLE1)
    image2 = ImageObj(INDUSTRYSAMPLE2)

    # check image resolutions
    ic = ImageComparison(image1, image2)
    return ic.checkImageResolutions()






class ImageBlock:
    def __init__(self, p1: list, p2: list) -> None:
        # insert row and column coordinates respectively
        self.p1 = p1
        self.p2 = p2

    def showPoints(self):

        print(self.p1)
        print(self.p2)

    def calculate(self):
        # call for calculating the alternate coordinates [leftTop , rightBottom]
        return [[self.p1[0], self.p2[1]], [self.p2[0], self.p1[1]]]


def testImageBlock():
    pass

    # bc = BlockCoordinates(p2, p3)
    # p1, p4 = bc.calcalate()
    # print(p1, p4)

    # bc1 = BlockCoordinates(p1, p4)
    # print(bc1.calcalate())

    # ib = ImageBlock(p1, p2, p3, p4)
    # ib.showPoints()


def testImageBlockComparsion(img1, img2, ib: ImageBlock):
    # p2, p3 = [962, 309], [558, 667]
    # bc = BlockCoordinates(p2, p3)
    # p1, p4 = bc.calcalate()
    # print(p1, p4)

    # bc1 = BlockCoordinates(p1, p4)
    # print(bc1.calcalate())

    # ib = ImageBlock(
    #     p1,
    #     p2,
    # )
    # ib.showPoints()

    # img1 = ImageObj(INDUSTRYSAMPLE1)
    # img2 = ImageObj(INDUSTRYSAMPLE2)

    img1 = img1.cropImage2([ib.p2[1], ib.p1[1]], [ib.p1[0], ib.p2[0]], False)
    img2 = img2.cropImage2([ib.p2[1], ib.p1[1]], [ib.p1[0], ib.p2[0]], False)

    img1 = ImageObj(img=img1)
    print(img1.shape)
    # img1.showImage(cv2.WINDOW_AUTOSIZE)
    img2 = ImageObj(img=img2)

    ic = ImageComparison(img1, img2)

    ic.imageSubtraction()
    # ic.showImages()
    # print(ic.meanSquareError())

    mse = int(ic.meanSquareError())

    if mse:
        print("THERE IS A DIFFERENCE")
        print(mse)
        # print(img1.shape)

        # finding Image Contours
        dst = ic.imageContour()
        # print(dst)

        # check mse

        # TOGGLE FOR SHOW IMAGES
        # ic.showImages()

        # return [ib.p2[1] + dst[0], ib.p1[1]], [ib.p1[0] + dst[1], ib.p2[0]]
        return [ib.p2[1], ib.p1[1]], [ib.p1[0], ib.p2[0]]

    else:
        print("NO DIFFERENCE AT ALL")


def testImageBlock2(img1, img2):

    # columns = [
    #     [551, 79],
    #     [944, 79],
    #     [1337, 79],
    #     [1733, 79],
    #     [2126, 79],
    #     [2519, 79],
    #     [2913, 79],
    #     [3229, 79],
    # ]
    # rows = [[277, 315], [277, 686], [277, 1055], [277, 1426], [277, 1794], [277, 2126]]

    columns = []
    rows = []

    differences = []

    print(img1.shape)
    for x in range(0, img1.shape[1], BLOCKSIZE):
        columns.append([x, 0])

    for y in range(0, img1.shape[0], BLOCKSIZE):
        rows.append([0, y])

    columns.append([img1.shape[1], 0])
    rows.append([0, img1.shape[0]])

    columns = columns[1:]
    rows = rows[1:]

    print(columns)
    print(rows)
    # return
    row = 1
    col = 1
    threads = []

    start = time.perf_counter()

    with concurrent.futures.ThreadPoolExecutor() as executer:

        for pr in rows:
            new_columns = []
            pn = pr
            for pc in columns:
                ib = ImageBlock(pn, pc)
                thread = executer.submit(testImageBlockComparsion, img1, img2, ib)
                threads.append(thread)

                # difference_coordinates = thread.result()
                # if difference_coordinates:
                #     print(difference_coordinates)
                #     differences.append(difference_coordinates)

                pn = ib.calculate()[1]
                new_columns.append(pn)

                print(f"{row} {col} = {pn}")
                col += 1

            # print(columns)
            row += 1
            columns = new_columns

    stop = time.perf_counter()

    for thread in threads:
        difference_coordinates = thread.result()
        if difference_coordinates:
            print(difference_coordinates)
            differences.append(difference_coordinates)

    print(differences)
    print(f"Time taken {round(stop - start , 2)} seconds. ")


if __name__ == "__main__":

    # testImageComparison()
    # testImageResolution()

    # to find out coordinates on image
    # img1 = ImageObj(INDUSTRYSAMPLE1)
    # img = img1.img
    # testImageCropping(img)

    # here
    img1 = ImageObj(INDUSTRYSAMPLE1)
    img2 = ImageObj(INDUSTRYSAMPLE2)
    testImageBlock2(img1, img2)
    # imgcheck = np.asarray(img1)
    # print(imgcheck)
    # highlight = np.zeros((img1.shape), dtype=np.int8)

    # print(img1.shape)
    # print(img2.shape)

    # testImageBlockComparsion()

    # img = ImageObj()
