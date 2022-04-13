import cv2
import numpy as np
import os

# PATHS TO COMPARE IMAGES
TEST_FILE = r"images\test1.jpg"
COMPARE_FILE = r"images\test1c.jpg"
DIFFERENT_COMPARE_FILE = r"images\images.png"

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
class Image:
    def __init__(self, img_path=None):
        self.img_path = img_path
        self.img = cv2.imread(self.img_path)

    def checkImage(self):

        if not os.path.isfile(self.img_path):
            return False
        return True

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


class ImageComparison:
    def __init__(self, img1=None, img2=None):
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

    def ImageSubtraction(self):

        if not self.checkImageResolutions():
            self.img1.resizeImage(RESIZE_RESOLUTION)
            self.img2.resizeImage(RESIZE_RESOLUTION)

        # print("NEW RESOLUTIONS = ", self.img1.getResolution())
        # print("NEW RESOLUTIONS = ", self.img2.getResolution())

        # self.img1 = np.array(self.img1)
        # self.img2 = np.array(self.img2)

        # self.img1 = np.int32(self.img1)
        # self.img2 = np.int32(self.img2)

        img1data = np.asarray(self.img1)
        img2data = np.asarray(self.img2)

        # image_difference = cv2.subtract(self.img1, self.img2,image_difference)
        # image_difference = cv2.subtract(self.img1, self.img2)
        image_difference = cv2.subtract(img1data, img2data)

        with open(r"imagearrayfile.txt", "w") as wt:
            wt.writelines(map(str, image_difference))

        # cv2.imshow(image_difference)
        b, g, r = cv2.split(image_difference)
        print(f"B = {b} , G = {g} , R = {r}")

        # img3 = self.img1 - self.img2

        # print(img3)


class MSE(ImageComparison):
    def __init__(self, img1, img2):
        self.img1 = img1
        self.img2 = img2

    def MeanSquareError(self):

        # if not self.checkImageResolutions():
        #     self.img1.resizeImage(RESIZE_RESOLUTION)
        #     self.img2.resizeImage(RESIZE_RESOLUTION)

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

    image1 = Image(TEST_FILE)

    image2 = Image(COMPARE_FILE)

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

    # ic = ImageComparison(image1, image2)
    # ic.checkImageResolutions()
    # ic.ImageSubtraction()
    ic = MSE(image1, image2)
    print("MEAN SQUARE ERROR : ", ic.MeanSquareError())
