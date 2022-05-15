from PIL import Image, ImageChops

TEST_FILE = r"images\test1.jpg"
COMPARE_FILE = r"images\test1c.jpg"
DIFFERENT_COMPARE_FILE = r"images\images.png"

print("Loading Images")
img1 = Image.open(TEST_FILE)
img2 = Image.open(DIFFERENT_COMPARE_FILE)
# img2 = Image.open(COMPARE_FILE)


print("Comparing images")
diff = ImageChops.difference(img1, img2)

print("Done !")
print(diff.getbbox())
if diff.getbbox():
    diff.show()
