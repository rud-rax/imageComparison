import cv2

img= cv2.imread(r"industrySample/page0.jpg")

def click_event(event, x, y, flags, params):

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

if __name__ == "__main__" :
    testImageCropping(img)