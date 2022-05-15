import numpy as np
from PIL import Image

TEST_FILE = r"images\test1.jpg"

image = Image.open(TEST_FILE)
# print(image.size)
height, width = image.size
numpydata = np.asarray(image)

# canvas = Image.fromarray(np.zeros((height, width, 3), np.uint8))
# canvas.show()

# contours = []
# for row in numpydata[:1]:
#     for col in row:
#         r, b, g = col
#         print(f"R {r} B {b} G {g}")
print(numpydata)
with open(r"imagearrayfile.txt", "w") as wt:
    wt.writelines(map(str, numpydata))
