import cv2 
import numpy as np
param=[]
bufferX1=100
bufferY1=50
bufferX2=30
bufferY2= 40

class extractImageBorder:
    
    def __init__(self,img_path) -> None:
        if not img_path:
            print("Find not found Error!")
            raise FileNotFoundError

        self.imgPath=img_path

    def Processing(img):
       
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        blurr=cv2.GaussianBlur(gray,(3,3),0)
        _,thresh=cv2.threshold(blurr,5,255,cv2.THRESH_BINARY)
        thresh=cv2.Canny(thresh,100,200)

        return thresh
        
    def extractBorder(self,display=True):
        img=cv2.imread(self.imgPath)

        thresh=extractImageBorder.Processing(img)

        #Detecting Contours
        contours,_=cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            (x,y,w,h)=cv2.boundingRect(contour)
            #Adding a buffer to the image
            X=x+bufferX1
            Y=y+bufferY1
            X1=x-bufferX2
            Y1=y-bufferY2
            if cv2.contourArea(contour)<100000:
                continue
            img=cv2.rectangle(img,(X,Y),(X1+w,Y1+h),(0,0,255),2)
            #Cropping of the image
            cropped_image=img[Y:Y1+h,X:X1+w]

        if display:
            cv2.namedWindow("Image",cv2.WINDOW_NORMAL)
            cv2.imshow("Image",cropped_image)
            
            k=cv2.waitKey()
        if k==ord('s'):
            cv2.imwrite('industrySample/page10Cropped.jpg',cropped_image)
        
        cv2.destroyAllWindows()
        return cropped_image

if __name__=="__main__":
    img_path="industrySample/page10.jpg"
    img=extractImageBorder(img_path)
    img.extractBorder()
