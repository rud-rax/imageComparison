from ICM import * 
import matplotlib.pyplot as plt
import numpy as np
import cv2

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

BLOCKSIZE = 200
def imageContour(img1, img2):
    diff = cv2.absdiff(img1, img2)
    grayscale = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    print("Image Resolution1 = ", img1.shape)

    blurr = cv2.GaussianBlur(gray, (3, 3), 0)
    print("Image Resolution2 = ", img1.shape)

    _, thresh = cv2.threshold(blurr, 10, 255, cv2.THRESH_BINARY)
    print("Image Resolution 3= ", img1.shape)

    dilated = cv2.erode(thresh, None, iterations=3)

    # Finding Contour:
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    print("Image Resolution4 = ", img1.shape)

    dst = cv2.drawContours(img1, contours, -1, (127, 127, 127), 2)
    print("Image Resolution5 = ", img1.shape)


    for contour in contours:
        # print("p")
        (x, y, w, h) = cv2.boundingRect(contour)
        print("Image Resolution6= ",img1.shape)
         

        if cv2.contourArea(contour) < 100:
            continue
        dst = cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 0, 255), 2)

    print("Image Resolution7 = ", img1.shape)
    #cv2.imshow("DST", dst)
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


def click_event(img , event, x, y, flags, params):
    # def click_event(event, x, y, flags, params):

    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:

        # displaying the coordinates
        # on the Shell
        print(x, " ", y)

        # displaying the coordinates
        # on the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, str(x) + "," + str(y), (x, y), font, 1, (255, 0, 0), 2)
        cv2.imshow("image", img)

    # checking for right mouse clicks
    if event == cv2.EVENT_RBUTTONDOWN:

        # displaying the coordinates
        # on the Shell
        print(x, " ", y)

        # displaying the coordinates
        # on the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        b = img[y, x, 0]
        g = img[y, x, 1]
        r = img[y, x, 2]
        cv2.putText(
            img, str(b) + "," + str(g) + "," + str(r), (x, y), font, 1, (255, 255, 0), 2
        )
        cv2.imshow("image", img)


def testImageCropping(img1):

    # image1 = ImageObj(INDUSTRYSAMPLE1)
    # image2 = ImageObj(INDUSTRYSAMPLE2)

    # if not testImageResolution():
    #     return

    # image1.cropImage2
    cv2.namedWindow("image", cv2.WINDOW_NORMAL)

    cv2.imshow("image", img1)
    cv2.setMouseCallback("image", click_event)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


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
    #print(img1.shape)
    # img1.showImage(cv2.WINDOW_AUTOSIZE)
    img2 = ImageObj(img=img2)

    ic = ImageComparison(img1, img2)

    ic.imageSubtraction()
    # ic.showImages()
    # print(ic.meanSquareError())

    mse = int(ic.meanSquareError())

    if mse:
        #print("THERE IS A DIFFERENCE")
        #print(mse)
        # print(img1.shape)

        # finding Image Contours
        dst = imageContour(img1.img, img2.img)
        #print(dst)

        # check mse

        # TOGGLE FOR SHOW IMAGES
        print("Image Resolution in blockcomp= ", img1.shape)

        ic.showImages()

        #return [ib.p2[1] + dst[0], ib.p1[1]], [ib.p1[0] + dst[1], ib.p2[0]]

        return [ib.p2[1], ib.p1[1]], [ib.p1[0], ib.p2[0]]

    else:
        pass
        #print("NO DIFFERENCE AT ALL")

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

    for x in range(277 , 3229 , BLOCKSIZE) :
        columns.append([x , BLOCKSIZE])

    for y in range(79 , 2126 , BLOCKSIZE) :
        rows.append([BLOCKSIZE , y])

    columns.append([3229 , BLOCKSIZE])
    rows.append([BLOCKSIZE , y])

    


    row = 1
    col = 1
    for pr in rows:
        new_columns = []
        pn = pr
        for pc in columns:
            ib = ImageBlock(pn, pc)
            testImageBlockComparsion(img1, img2, ib)
            # break

            pn = ib.calculate()[1]
            new_columns.append(pn)

            print(f"{row} {col} = {pn}")
            col += 1

        print(columns)
        row += 1
        columns = new_columns


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

    # testImageBlockComparsion()

    # img = ImageObj()
