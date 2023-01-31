from extractObjects1 import *

IMAGE_CONFIG_FILE_PATH = r"extractObjectsFeature/ImageConfigFiles/"
configFilesDirList = os.listdir(IMAGE_CONFIG_FILE_PATH)

print(configFilesDirList)
for i,file in enumerate(configFilesDirList) :
    print(i,file)

i = int(input("Enter file number --> "))
j = input("Do you want to load Default Config ? [Y/n] ")

if j and str.lower(j) == "n": 
    j = False
else :
    j = True

file = configFilesDirList[i]

print(f"Extract file config path = {IMAGE_CONFIG_FILE_PATH+file} , Default Config = {j}")

ideo = ImageDrawingExtraction(IMAGE_CONFIG_FILE_PATH+file, j)
ideo.extractObjects()