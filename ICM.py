import cv2
import numpy as np
import os
from PIL import Image
import concurrent.futures
import time

# CODE FOR VERSION 2
# from extractObjectsFeature import extractObjects1




# PATHS TO COMPARE IMAGES
TEST_FILE = r"images\test1.jpg"
COMPARE_FILE = r"images\test1c.jpg"
# DIFFERENT_COMPARE_FILE = r"images\images.png"
# DIFFERENT_TEST_FILE_1 = r"images\test1.1.jpeg"
DIFFERENT_TEST_FILE_2 = r"images\test1.2.jpeg"

# ICM_test2 global variables
DIFFIMAGE = r"images\diff_image1.jpg"

INDUSTRYSAMPLE1 = r"industrySample/page0.jpg"
INDUSTRYSAMPLE2 = r"industrySample/page10.jpg"
i1 = cv2.imread(INDUSTRYSAMPLE1)

BLOCKSIZE = 200
MSE_THRESHOLD = 1000


# SHAPES IMAGES PATH (TESTING PURPOSE)

# CIRCLE_IMAGE = r"shapes_iamges\circle.jpg"
# LONG_IMAGE = r"shapes_images\long_1x3.jpg"
# QUAD_IMAGE = r"shapes_images\quad.jpg"
# TRI_IMAGE = r"shapes_images\tri_255x217.jpg"


# SET BELOW VARIABLE TO FALSE IF YOU DONT WANT TO CHECK FOR IMAGE FILES
CHECK_IMAGE_FILES = False


# CHANGE RESIZING AND SCALING VARIABLESimg_path
RESIZE_RESOLUTION = (1000, 650)
SCALE_PERCENTAGE = 150


# DEFINED CUSTOM ERRORS


class DifferentResolutionError(Exception):
    """Images have different resolutions."""

    pass


# IMAGE COMPARISON METHODS
class ImageObj:
    def __init__(self, img_path=None, img=None):
        self.img_path = img_path
        self.img = img
        if self.img_path:
            self.img = cv2.imread(self.img_path)
        self.shape = None
        self.getShape()

    def checkImage(self):

        # if not os.path.isfile(self.img_path):
        #     return False
        # return True
        pass

    def getShape(self):
        self.shape = self.img.shape

    def getResolution(self):
        try:
            if self.checkImage():
                return self.img.shape
        except FileNotFoundError as e:
            #print(e.__doc__)
            pass

    def resizeImage(self, reso=RESIZE_RESOLUTION, scale=None):
        if scale:
            reso = (
                int(self.img.shape[1] * scale // 100),
                int(self.img.shape[0] * scale // 100),
            )
            self.img = cv2.resize(self.img, reso)
        elif reso:
            self.img = cv2.resize(self.img, reso)

    def showImage(self, window_size_param=cv2.WINDOW_NORMAL):
        cv2.namedWindow("Image", window_size_param)
        cv2.imshow("Image", self.img)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def checkNegetiveThreshold(self, threshold=50):

        # print("DIFFERENCES AT -")

        numImg = np.asarray(self.img)
        diffList = []

        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                b, g, r = numImg[i][j]

                if b >= threshold or g >= threshold or r >= threshold:

                    # print(f"{i} {j}")
                    diffList.append((i, j))

        return diffList

    def cropImage(self, threshold=240):

        cropParam = []

        numImg = np.asarray(self.img)

        # with open("imageData.txt", "w") as imgfile:
        #     for line in numImg:
        #         lines = "-".join(list(map(str, line)))
        #         imgfile.writelines(lines)

        # print(numImg[0])

        endLoop = False

        for i in range(self.shape[0]):
            if not endLoop:
                for j in range(self.shape[1]):
                    b, g, r = numImg[i][j]
                    if b <= threshold and g <= threshold and r <= threshold:
                        # print(f"{b} {g} {r} @ {i} {j}")
                        # self.markPixel(i, j, 10, [255, 0, 0])
                        cropParam.append((i, j))
                        endLoop = True
                        break

        endLoop = False
        for i in np.arange(self.shape[0] - 1, 0, -1):
            if not endLoop:
                for j in np.arange(self.shape[1] - 1, 0, -1):
                    b, g, r = numImg[i][j]
                    if b <= threshold and g <= threshold and r <= threshold:
                        print(f"{b} {g} {r} @ {i} {j}")
                        # self.markPixel(i, j, 10, [255, 0, 0])
                        cropParam.append((i, j))
                        endLoop = True
                        break

        endLoop = False
        for j in range(self.shape[1]):
            if not endLoop:
                for i in range(self.shape[0]):
                    b, g, r = numImg[i][j]

                    if b <= threshold and g <= threshold and r <= threshold:
                        # print(f"{b} {g} {r} @ {i} {j}")
                        # self.markPixel(i, j, 10, [255, 0, 0])
                        cropParam.append((i, j))
                        endLoop = True
                        break

        endLoop = False
        for j in range(self.shape[1] - 1, 0, -1):
            if not endLoop:
                for i in range(self.shape[0] - 1, 0, -1):
                    b, g, r = numImg[i][j]

                    if b <= threshold and g <= threshold and r <= threshold:
                        print(f"{b} {g} {r} @ {i} {j}")
                        # self.markPixel(i, j, 10, [255, 0, 0])
                        cropParam.append((i, j))
                        endLoop = True
                        break

        self.markPixel(cropParam, 10, [255, 0, 0])

        self.cropImage2(
            (cropParam[0][0], cropParam[1][0]), (cropParam[2][1], cropParam[3][1]), True
        )

    def markPixel(self, points, trad=0, tcolor=[0, 0, 0]):

        # Draw a red circle with zero radius and -1 for filled circle

        for i, j in points:
            markedImg = cv2.circle(
                self.img, (j, i), radius=trad, color=tcolor, thickness=3
            )
        # self.img = cv2.circle(
        #     self.img, (10, 10), radius=trad, color=tcolor, thickness=3
        # )

        cv2.imshow("Mark Point", markedImg)
        cv2.waitKey(0)
        # cv2.destroyAllWindows()

    def cropImage2(
        self, start: list, stop: list, inplace: bool = False, showbool: bool = False
    ):

        print(start, stop)

        start_i, start_j = start
        stop_i, stop_j = stop

        croppedImg = self.img[start_i:start_j, stop_i:stop_j]
        if showbool:
            self.showImage()

            cv2.imshow("Cropped Image", croppedImg)

        if inplace:
            self.img = croppedImg

        return croppedImg
        # cv2.imshow("Image", self.img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()




class ImageComparison:
    def __init__(self, img1: ImageObj, img2: ImageObj):
        self.img1 = img1
        self.img2 = img2

    def showImages(self):
        cv2.imshow("Image1", self.img1.img)
        cv2.imshow("Image2", self.img2.img)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def checkImageResolutions(self):
        try:
            if self.img1.checkImage() and self.img2.checkImage():

                if self.img1.getResolution() == self.img2.getResolution():
                    # print("Images have the same Resolution !")
                    return True

                else:
                    raise DifferentResolutionError

        except DifferentResolutionError as e:
            print(e.__doc__)
            return False

    def imageSubtraction(self, save_fig=False):

        # self.img1.cropImage(230)
        # self.img2.cropImage(230)

        # if not self.checkImageResolutions():
        #     self.img1.resizeImage(RESIZE_RESOLUTION)
        #     self.img2.resizeImage(RESIZE_RESOLUTION)

        # print("NEW RESOLUTIONS = ", self.img1.getResolution())
        # print("NEW RESOLUTIONS = ", self.img2.getResolution())

        # self.img1 = np.array(self.img1)
        # self.img2 = np.array(self.img2)

        # self.img1 = np.int32(self.img1)
        # self.img2 = np.int32(self.img2)

        img1data = np.asarray(self.img1.img)
        img2data = np.asarray(self.img2.img)

        # image_difference = cv2.subtract(self.img1, self.img2,image_difference)
        # image_difference = cv2.subtract(self.img1, self.img2)
        image_difference = cv2.subtract(img1data, img2data)
        # cv2.imwrite(f"images/imagediff",image_difference)

        # with open(r"imagearrayfile.txt", "w") as wt:
        #     wt.writelines(map(str, image_difference))

        # cv2.imshow(image_difference)

        canvas = Image.fromarray(image_difference)
        # canvas.show()

        if save_fig:
            SAVE_IMG_PATH = r"images/diff_image1.jpg"
            canvas.save(SAVE_IMG_PATH)

            diffImg = ImageObj(SAVE_IMG_PATH)

            diffImg.checkNegetiveThreshold()
            #print(diffImg.getResolution())
        # b, g, r = cv2.split(image_difference)
        # print(f"B = {b} , G = {g} , R = {r}")

        # img3 = self.img1 - self.img2

        # print(img3)

    def meanSquareError(self):

        if not self.checkImageResolutions():
            self.img1.resizeImage(RESIZE_RESOLUTION)
            self.img2.resizeImage(RESIZE_RESOLUTION)

        # print("NEW RESOLUTIONS = ", self.img1.getResolution())
        # print("NEW RESOLUTIONS = ", self.img2.getResolution())

        img1 = cv2.cvtColor(self.img1.img, cv2.COLOR_BGR2GRAY)
        img2 = cv2.cvtColor(self.img2.img, cv2.COLOR_BGR2GRAY)

        err = np.sum((img1.astype("float") - img2.astype("float")) ** 2)
        err /= float(img1.shape[0] * img1.shape[1])

        return err

    def imageContour(self):
        diff = cv2.absdiff(self.img1.img, self.img2.img)
        grayscale = cv2.cvtColor(self.img1.img, cv2.COLOR_BGR2GRAY)

        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blurr = cv2.GaussianBlur(gray, (3, 3), 0)
        _, thresh = cv2.threshold(blurr, 10, 255, cv2.THRESH_BINARY)
        dilated = cv2.erode(thresh, None, iterations=3)

        # Finding Contour:
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        dst = cv2.drawContours(self.img1.img, contours, -1, (127, 127, 127), 2)

        for contour in contours:
            # print("p")
            (x, y, w, h) = cv2.boundingRect(contour)
            if cv2.contourArea(contour) < 100:
                continue
            dst = cv2.rectangle(self.img2.img, (x, y), (x + w, y + h), (0, 0, 255), 2)

        print("Image Resolution = ", self.img1.shape)
        # cv2.imshow("DST", dst)
        return x, y, w, h


# INSERT ICM_TEST2 CODE HERE

class ImageBlock:
    def __init__(self, p1: list, p2: list) -> None:
        # insert row and column coordinates respectively
        self.p1 = p1
        self.p2 = p2

    def showPoints(self):
        pass

        # print(self.p1)
        # print(self.p2)

    def calculate(self):
        # call for calculating the alternate coordinates [leftTop , rightBottom]
        return [[self.p1[0], self.p2[1]], [self.p2[0], self.p1[1]]]



def imageContour(img1, img2):
    diff = cv2.absdiff(img1, img2)
    grayscale = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    # print("Image Resolution1 = ", img1.shape)

    blurr = cv2.GaussianBlur(gray, (3, 3), 0)
    # print("Image Resolution2 = ", img1.shape)

    _, thresh = cv2.threshold(blurr, 10, 255, cv2.THRESH_BINARY)
    # ("Image Resolution 3= ", img1.shape)

    dilated = cv2.erode(thresh, None, iterations=3)

    # Finding Contour:
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # print("Image Resolution4 = ", img1.shape)

    dst = cv2.drawContours(img1, contours, -1, (127, 127, 127), 2)
    # print("Image Resolution5 = ", img1.shape)

    for contour in contours:
        # print("p")
        (x, y, w, h) = cv2.boundingRect(contour)
        # print("Image Resolution6= ",img1.shape)

        if cv2.contourArea(contour) < 100:
            continue
        dst = cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # print("Image Resolution7 = ", img1.shape)
    # cv2.imshow("DST", dst)
    return x, y, w, h




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
    # print(img1.shape)
    # img1.showImage(cv2.WINDOW_AUTOSIZE)
    img2 = ImageObj(img=img2)

    ic = ImageComparison(img1, img2)

    ic.imageSubtraction()
    # ic.showImages()
    # print(ic.meanSquareError())

    mse = int(ic.meanSquareError())

    if mse:
        # print("THERE IS A DIFFERENCE")
        # print(mse)
        # print(img1.shape)

        # finding Image Contours
        dst = imageContour(img1.img, img2.img)
        # print(dst)

        # check mse

        # TOGGLE FOR SHOW IMAGES
        # print("Image Resolution in blockcomp= ", img1.shape)

        # ic.showImages()

        # return [ib.p2[1] + dst[0], ib.p1[1]], [ib.p1[0] + dst[1], ib.p2[0]]

        return [ib.p2[1], ib.p1[1]], [ib.p1[0], ib.p2[0]]

    else:
        pass
        # print("NO DIFFERENCE AT ALL")



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

    # print(img1.shape)
    for x in range(0, img1.shape[1], BLOCKSIZE):
        columns.append([x, 0])

    for y in range(0, img1.shape[0], BLOCKSIZE):
        rows.append([0, y])

    columns.append([img1.shape[1], 0])
    rows.append([0, img1.shape[0]])

    columns = columns[1:]
    rows = rows[1:]

    # print(columns)
    # print(rows)
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

                # print(f"{row} {col} = {pn}")
                col += 1

            # print(columns)
            row += 1
            columns = new_columns

    stop = time.perf_counter()

    for thread in threads:
        difference_coordinates = thread.result()
        if difference_coordinates:
            # print(difference_coordinates)
            differences.append(difference_coordinates)

    # print(differences)

    print(f"Time taken {round(stop - start , 2)} seconds. ")
    return differences


def inOne(cordinates, img1, img2):
    # print(cordinates)
    for i in range(len(cordinates)):
        # converting images to pixels
        pixel_array1 = np.asarray(img1)
        pixel_array2 = np.asarray(img2)

        y1 = cordinates[i][0][0]
        y2 = cordinates[i][0][1]
        x1 = cordinates[i][1][0]
        x2 = cordinates[i][1][1]

        dst = cv2.rectangle(img1, (x1, y1), (x2, y2), (0, 0, 0), 10)
        dst = cv2.rectangle(img2, (x1, y1), (x2, y2), (0, 0, 0), 10)
        pixel_array1[y1:y2, x1:x2, 2] = 255
        pixel_array2[y1:y2, x1:x2, 2] = 255

    # print(img1.shape[:2])
    # pixel_array=np.asarray(img1)

    # zeros = np.zeros(img1.shape[:2], dtype="uint8")
    # (B,G,R)=cv2.split(dst)
    # G[x1 : x2 , y1 : y2] = 0
    cv2.namedWindow("Image1", cv2.WINDOW_NORMAL)
    cv2.namedWindow("Image2", cv2.WINDOW_NORMAL)
    cv2.imshow("Image1", img1)
    cv2.imshow("Image2", img2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    filepath1 = r"industrySample/img1.jpg"
    filepath2 = r"industrySample/img2.jpg"
    cv2.imwrite(filepath1, img1)
    cv2.imwrite(filepath2, img2)
    images = [Image.open("industrySample/" + f) for f in ["img1.jpg", "img2.jpg"]]
    pdf_path = "Output.pdf"

    images[0].save(
        pdf_path, "PDF", resolution=100.0, save_all=True, append_images=images[1:]
    )



# CHECKING FILES BEFORE RUNNING THE CODE
def checkFile():

    print(f"Finding Files in {os.listdir()}")

    try:

        if not os.path.isfile(TEST_FILE):

            raise FileNotFoundError

        if not os.path.isfile(COMPARE_FILE):

            raise FileNotFoundError

        print("Both files found !")

    except FileNotFoundError:
        print(f"The required files are not found !")

    except Exception as e:
        print(e)



if __name__ == "__main__":

    if CHECK_IMAGE_FILES:
        checkFile()

    image1 = ImageObj(TEST_FILE)
    # image2 = ImageObj(DIFFERENT_COMPARE_FILE)
    # image2 = ImageObj(DIFFERENT_TEST_FILE_1)
    image2 = ImageObj(DIFFERENT_TEST_FILE_2)

    # image1 = ImageObj(QUAD_IMAGE)
    # image2 = ImageObj(TRI_IMAGE)

    image1.showImage()
    image2.showImage()

    # image1.showImage()
    # print(image1.img.shape[0])
    # print(image1.getResolution())

    # image1.resizeImage(RESIZE_RESOLUTION, scale=150)
    # image1.showImage()

    # print(image1.getResolution())

    # image1.checkImage()
    # image2.checkImage()

    # print(image1.getResolution())
    # print(image2.getResolution())

    # IMAGE SUBTRACTION TESTING

    ic = ImageComparison(image1, image2)
    ic.ImageSubtraction(save_fig=True)
    # ic.checkImageResolutions()

    # MSE TESTING
    # ic = MSE(image1, image2)
    print("MEAN SQUARE ERROR : ", ic.MeanSquareError())
