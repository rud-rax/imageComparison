import cv2
import configparser
import os

DEFAULT_CONFIG_FILE_PATH = r"extractObjectsFeature/config.ini"

class ImageDrawingExtraction :
    '''
    Used to extract multiple Mechanical Drawings from an Image

    1st parameter : Config file path of the Image
    (It is necessary to create config file of an image inorder to create an Object of this Class)

    2nd parameter : Boolean value to set the default config or not
    '''

    def __init__(self,config_path,defaultConfig = True) -> None:

        if not self.checkIfFileExists(config_path) :
            print("Image Config File Not Found")
            raise FileNotFoundError

        if not self.checkIfFileExists(DEFAULT_CONFIG_FILE_PATH) :
            print("Config File Not Found")
            raise FileNotFoundError

        self.config_path = config_path

        self.ipp = None
        self.filevar = None
        self.extract_roi = None

        self.loadConfigurationsForImagePreprocessing(defaultConfig)

        self.image = None
        self.original = None

    def checkIfFileExists(self,file) -> bool:
        '''
        Checks if the config file exists in the directory of not
        Image config file should be in 'ImageConfigFiles' directory
        Image preprocessing config file should be in 'extractObjectsFeature' directory
        '''
        return os.path.isfile(file) 

    def imagePreprocessing(self,display = False) :
        '''
        Image Preprocessing Methods are encapsulated in this method. Returns the preprocessed image
        '''

        KERNEL_SIZE_GAUSSIAN_BLUR  =  tuple(map(int,self.ipp['gaussian_blur_kernel_size'].split(",")))
        KERNEL_SIZE_STRUCTURING_ELEMENT = tuple(map(int,self.ipp['structuring_element_kernel_size'].split(",")))
        DILATE_ITERATIONS = int(self.ipp['dilate_iter'])

        # Convert Image into Greyscale
        gray = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)
        
        # Applied gaussian blur on the image (kernel size specified in config file)
        blur = cv2.GaussianBlur(gray, KERNEL_SIZE_GAUSSIAN_BLUR, 0)
        
        # Dilating the image (parameter are specifed in the config file)
        # Otsu's threshold is applied
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, KERNEL_SIZE_STRUCTURING_ELEMENT)

        if display :         
            cv2.imshow('Threshold Image', thresh)

        
        return cv2.dilate(thresh, kernel, iterations= DILATE_ITERATIONS)

    def findContoursOnImage(self,dilate) :
        '''
        Method used to find Contours on dilated image. Returns contours found on the image.
        '''

        # Find contours, obtain bounding box coordinates, and extract ROI
        cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return cnts[0] if len(cnts) == 2 else cnts[1]

    def extractFromContours(self,counter,image_number) -> None :
        '''
        Method used for cropping the contours from the image.
        '''

        # Creating Rectangle around the extracted Image Drawing
        x,y,w,h = cv2.boundingRect(counter)
        cv2.rectangle(self.image, (x, y), (x + w, y + h), (36,255,12), 2)

        # Cropping the extracted Image Drawing from the original Image
        ROI = self.original[y:y+h, x:x+w]

        # Checking if the extracted image passes the threshold (threshold specified in the config file)
        if len(ROI) > int(self.extract_roi['width']) and len(ROI[0]) > int(self.extract_roi['height']) :
            print(image_number,len(ROI) , len(ROI[0]))

            # Saving the image (save path specified in the config file)
            cv2.imwrite("{}/{}/{}-{}.png".format(self.filevar['save_path'],self.filevar['save_folder'],self.filevar['save_file_name'],image_number), ROI)

    def loadConfigurationsForImagePreprocessing(self,defaultConfig) -> None:
        '''
        Method used to extract parameters from the config file and set the instance variables
        Will be called automatically, when the object is created.
        '''

        defaultConfigobject = configparser.ConfigParser()

        # Reading default config file 
        defaultConfigobject.read(DEFAULT_CONFIG_FILE_PATH)

        # Extracting parameters from default config file
        self.ipp = defaultConfigobject['IMAGE_PREPROCESSING'] 
        self.extract_roi = defaultConfigobject['EXTRACT_ROI_THRESHOLD']

        configobject = configparser.ConfigParser()

        # Extracting parameters from Image config file of Image (specified during object creation)
        configobject.read(self.config_path)
        self.filevar = configobject['FILES_PATH']

        if not defaultConfig :
            # Executed only when 'defaultConfig' is set to False
            self.ipp = configobject['IMAGE_PREPROCESSING'] 
            self.extract_roi = configobject['EXTRACT_ROI_THRESHOLD']

    def extractObjects(self,display = False) :
        '''
        Extracts multiple mechanical drawings present in the image.

        1st parameter : Set true to show the operation performed on the image. (Set to False by default).
        '''

        # Reading the image
        self.image = cv2.imread(self.filevar['path'])
        if display : 
            # Displaying Image
            cv2.imshow('Image', self.image)

        
        # Create a copy of Image
        self.original = self.image.copy()
        
        # Perform Image Preprocessing Methods
        dilate = self.imagePreprocessing()

        if display : 
            # Displaying dilated image
            cv2.imshow('Dilated Image', dilate)
            cv2.waitKey()

        # Find contours on dilated Image
        contours = self.findContoursOnImage(dilate)
        
        # Making Directory for storing the extracted images
        if not os.path.isdir(self.filevar['save_path'] + self.filevar['save_folder']) :
            os.mkdir(self.filevar['save_path'] + self.filevar['save_folder'])

        img_num = 0
        for contour in contours:
            self.extractFromContours(contour,img_num)
            img_num += 1


if __name__ == "__main__" :

    print(DEFAULT_CONFIG_FILE_PATH)
    ideo = ImageDrawingExtraction(r"extractObjectsFeature/ImageConfigFiles/page0config.ini",False)
    ideo.extractObjects()