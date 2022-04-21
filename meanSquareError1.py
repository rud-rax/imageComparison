from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2


def mse(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err


def compare_images(imageA, imageB, title):

    m = mse(imageA, imageB)
    s = ssim(imageA, imageB)

    fig = plt.figure(title)
    plt.suptitle("MSE: %.2f, SSIM: %.2f" % (m, s))

    ax = fig.add_subplot(1, 2, 1)

    plt.imshow(imageA, cmap=plt.cm.gray)
    plt.axis("off")

    ax = fig.add_subplot(1, 2, 2)

    plt.imshow(imageB, cmap=plt.cm.gray)
    plt.axis("off")

    plt.show()


TEST_FILE = r"images\test1.jpg"
COMPARE_FILE = r"images\test1c.jpg"
DIFFERENT_COMPARE_FILE = r"images\images.png"
original = cv2.imread(TEST_FILE)
contrast = cv2.imread(COMPARE_FILE)
shopped = cv2.imread(DIFFERENT_COMPARE_FILE)


# convert the images to grayscale
original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
contrast = cv2.cvtColor(contrast, cv2.COLOR_BGR2GRAY)
shopped = cv2.cvtColor(shopped, cv2.COLOR_BGR2GRAY)


print(original.shape)

shopped = cv2.resize(shopped, (original.shape[1], original.shape[0]))


fig = plt.figure("Images")


images = ("Original", original), ("Contrast", contrast), ("Photoshopped", shopped)

for (i, (name, image)) in enumerate(images):

    ax = fig.add_subplot(1, 3, i + 1)
    ax.set_title(name)
    plt.imshow(image, cmap=plt.cm.gray)
    plt.axis("off")

plt.show()


compare_images(original, original, "Original vs. Original")
compare_images(original, contrast, "Original vs. Contrast")
compare_images(original, shopped, "Original vs. Photoshopped")
