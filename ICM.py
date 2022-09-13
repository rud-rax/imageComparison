import cv2
import numpy as np
import os
from PIL import Image


# PATHS TO COMPARE IMAGES
TEST_FILE = r"images\test1.jpg"
COMPARE_FILE = r"images\test1c.jpg"
DIFFERENT_COMPARE_FILE = r"images\images.png"
DIFFERENT_TEST_FILE_1 = r"images\test1.1.jpeg"
DIFFERENT_TEST_FILE_2 = r"images\test1.2.jpeg"


# SHAPES IMAGES PATH (TESTING PURPOSE)

CIRCLE_IMAGE = r"shapes_iamges\circle.jpg"
LONG_IMAGE = r"shapes_images\long_1x3.jpg"
QUAD_IMAGE = r"shapes_images\quad.jpg"
TRI_IMAGE = r"shapes_images\tri_255x217.jpg"


# SET BELOW VARIABLE TO FALSE IF YOU DONT WANT TO CHECK FOR IMAGE FILES
CHECK_IMAGE_FILES = False


# CHANGE RESIZING AND SCALING VARIABLES
RESIZE_RESOLUTION = (1000, 650)
SCALE_PERCENTAGE = 150


# DEFINED CUSTOM ERRORS


class DifferentResolutionError(Exception):
    """Images have different resolutions."""

    pass


# IMAGE COMPARISON METHODS
class ImageObj:
    def __init__(self, img_path=None):
        self.img_path = img_path
        self.img = cv2.imread(self.img_path)
        self.shape = None
        self.getShape()

    def checkImage(self):

        if not os.path.isfile(self.img_path):
            return False
        return True

    def getShape(self):
        self.shape = self.img.shape

    def getResolution(self):
        try:
            if self.checkImage():
                return self.img.shape
        except FileNotFoundError as e:
            print(e.__doc__)

    def resizeImage(self, reso=RESIZE_RESOLUTION, scale=None):
        if scale:
            reso = (
                int(self.img.shape[1] * scale // 100),
                int(self.img.shape[0] * scale // 100),
            )
            self.img = cv2.resize(self.img, reso)
        elif reso:
            self.img = cv2.resize(self.img, reso)

    def showImage(self):
        cv2.imshow("Image", self.img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def checkNegetiveThreshold(self, threshold=50):

        print("DIFFERENCES AT -")

        numImg = np.asarray(self.img)
        diffList = []

        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                b, g, r = numImg[i][j]

                if b >= threshold or g >= threshold or r >= threshold:

                    print(f"{i} {j}")
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
                        print(f"{b} {g} {r} @ {i} {j}")
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
                        print(f"{b} {g} {r} @ {i} {j}")
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

    def cropImage2(self, start, stop, inplace=False):

        print(start, stop)

        start_i, start_j = start
        stop_i, stop_j = stop

        croppedImg = self.img[start_i:start_j, stop_i:stop_j]
        if inplace:
            self.img = croppedImg

        cv2.imshow("Cropped Image", self.img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


class ImageComparison:
    def __init__(self, img1: ImageObj, img2: ImageObj):
        self.img1 = img1
        self.img2 = img2

    def checkImageResolutions(self):
        try:
            if self.img1.checkImage() and self.img2.checkImage():

                if self.img1.getResolution() == self.img2.getResolution():
                    print("Images have the same Resolution !")
                    return True

                else:
                    raise DifferentResolutionError

        except DifferentResolutionError as e:
            print(e.__doc__)
            return False

    def ImageSubtraction(self, save_fig=False):

        self.img1.cropImage(230)
        self.img2.cropImage(230)

        if not self.checkImageResolutions():
            self.img1.resizeImage(RESIZE_RESOLUTION)
            self.img2.resizeImage(RESIZE_RESOLUTION)

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

        with open(r"imagearrayfile.txt", "w") as wt:
            wt.writelines(map(str, image_difference))

        # cv2.imshow(image_difference)

        canvas = Image.fromarray(image_difference)
        canvas.show()

        if save_fig:
            SAVE_IMG_PATH = r"images/diff_image1.jpg"
            canvas.save(SAVE_IMG_PATH)

            diffImg = ImageObj(SAVE_IMG_PATH)

            diffImg.checkNegetiveThreshold()
            print(diffImg.getResolution())
        # b, g, r = cv2.split(image_difference)
        # print(f"B = {b} , G = {g} , R = {r}")

        # img3 = self.img1 - self.img2

        # print(img3)

    def MeanSquareError(self):

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
