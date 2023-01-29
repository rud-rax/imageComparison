
from extractObjects1 import *


IMAGE_CONFIG_FILE_PATH = r"extractObjectsFeature/ImageConfigFiles/"
configFilesDirList = os.listdir(IMAGE_CONFIG_FILE_PATH)

print(configFilesDirList)
for i,file in enumerate(configFilesDirList) :
    print(i,file)

i = int(input("Enter file number --> "))
file = configFilesDirList[i]

print(IMAGE_CONFIG_FILE_PATH+file)
# configobject = configparser.ConfigParser()
ideo = ImageDrawingExtraction(IMAGE_CONFIG_FILE_PATH+file)
ideo.extractObjects()