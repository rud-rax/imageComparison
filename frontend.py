from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from pdf2image import convert_from_path
# import qpageview
import sys
import os
from ICM_test2 import *


class dropImageLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setText("\n\n Drop Image Here\n\n")
        self.setStyleSheet("border: 4px dashed grey")
        self.setFixedHeight(400)

    def setPixmap(self, image):
        super().setPixmap(image)


class ImageLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)

    def setPixmap(self, image):
        super().setPixmap(image)


class COMPARE(QWidget):
    def __init__(self):
        self.img1 = ""  # path for image 1
        self.img2 = ""  # path for image 2
        self.count = 0

        super().__init__()
        self.setWindowTitle("Drop Images")
        windowSize = str(self.size())
        # windowDimensions = int(windowSize.split("(")[1].split(")")[0].split(", "))
        windowDimensions = list(map(int, windowSize.split("(")[1].split(")")[0].split(", ")))
        print(windowDimensions)

        self.setAcceptDrops(True)

        self.pccoelogo = ImageLabel()
        self.set_image(self.pccoelogo, "logo/PCCoELOGO.png")
        self.pccoelogo.setFixedSize(100,50)
        self.pccoelogo.setAlignment(Qt.AlignRight)

        self.companylogo = ImageLabel()
        self.set_image(self.companylogo, "logo/CompanyLOGO.png")
        self.companylogo.setFixedSize(100,50)
        self.companylogo.setAlignment(Qt.AlignRight)

        self.appname = QLabel()
        self.appname.setText("Name of Application")
        self.appname.setFixedHeight(100)
        self.appname.setAlignment(Qt.AlignLeft)
        self.appname.setStyleSheet("color: red;")

        self.applogo = ImageLabel()
        self.set_image(self.applogo, "logo/PCCoELOGO.png")
        self.applogo.setFixedSize(100,100)
        self.applogo.setAlignment(Qt.AlignLeft)

        self.imageLabel1 = dropImageLabel()
        self.imageLabel2 = dropImageLabel()
        self.imageLabel2.hide()

        mainlayout = QVBoxLayout()
        mainlayout.setContentsMargins(50,50,50,50)
        header = QHBoxLayout()
        header.addWidget(self.applogo)
        # header.addWidget(self.appname)
        
        nameMenu = QVBoxLayout()
        nameMenu.addWidget(self.appname)

        self.menuBar = QMenuBar()
        homeMenu = self.menuBar.addMenu("&Home")
        compareMenu = self.menuBar.addMenu("&Compare")
        contactMenu = self.menuBar.addMenu("&Contact")
        # header.addWidget(self.menuBar)
        nameMenu.addWidget(self.menuBar)

        header.addLayout(nameMenu)
        header.addWidget(self.companylogo)
        header.addWidget(self.pccoelogo)

        
        
        layout1 = QVBoxLayout()
        layout2 = QHBoxLayout()

        layout2.addWidget(self.pccoelogo)
        # layout2.addWidget(self.APPname)
        layout2.addWidget(self.companylogo)

        layout1.addLayout(layout2)

        layout1.addWidget(self.imageLabel1)
        self.imageLabel1.setText("\n\n Drop Original Image Here \n\n")

        layout1.addWidget(self.imageLabel2)
        self.imageLabel2.setText("\n\n Drop Created Image Here \n\n")
        self.imageLabel2.hide()

        self.browseButton = QPushButton("Browse")
        layout1.addWidget(self.browseButton, 1)
        self.browseButton.setEnabled(True)
        file_path = self.browseButton.clicked.connect(self.getImage)
        # print(file_path)
        if self.count == 1:
            self.img2 = file_path
            print(self.img2)
        elif self.count == 0:
            self.img1 = file_path
            print(self.img1)

        self.confirmButton = QPushButton("Confirm")
        layout1.addWidget(self.confirmButton, 1)
        self.confirmButton.setEnabled(False)
        self.confirmButton.clicked.connect(self.Confirm)

        self.compareButton = QPushButton("Compare")
        layout1.addWidget(self.compareButton, 1)
        self.compareButton.hide()
        self.compareButton.clicked.connect(self.Compare)

        # mainlayout.addLayout(header)
        self.setLayout(layout1)
        print(self.children)

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.Ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.Ignore()

    def dropEvent(self, event):

        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            file_path = event.mimeData().urls()[0].toLocalFile()
            
            if self.count == 1:
                file_path = self.set_image(self.imageLabel2, file_path)
                self.img2 = file_path
            elif self.count == 0:
                file_path = self.set_image(self.imageLabel1, file_path)
                self.img1 = file_path

            

            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText(
                    "Wrong format. Enter either an image file or a pdf file."
                )
                msg.setWindowTitle("Error")
                msg.addButton(QMessageBox.Ok)
                msg.exec_()

            self.confirmButton.setEnabled(True)

            event.accept()

        else:
            event.Ignore()

    def set_image(self, label, file_path):
        # label.setPixmap(QPixmap(file_path))

        if os.path.splitext(file_path)[-1].lower() == ".pdf":
            file_path = self.convertPDF2JPG(file_path, "page")
        
        if QPixmap(file_path) is not None:
            imageWidth, imageHeight = QPixmap(file_path).width(), QPixmap(file_path).height()
            labelWidth, labelHeight = label.width(), label.height()
            ratio = min(labelWidth / imageWidth, labelHeight / imageHeight)
            newWidth, newHeight = int(imageWidth * ratio), int(imageHeight * ratio)
            newPixmap = QPixmap(file_path).scaledToWidth(newWidth, Qt.TransformationMode.FastTransformation)
            label.setPixmap(newPixmap)
            return(file_path)


    def convertPDF2JPG(self, file_path, savename = ""):
        images = convert_from_path(file_path)
        for i in range(len(images)):
            new_file_path = "industrySample/" + savename + str(self.count) + ".jpg"
            images[i].save(new_file_path, "JPEG")
            return(new_file_path)
    
    def getImage(self):
        if self.count ==1:
            label = self.imageLabel2
        else:
            label = self.imageLabel1
        fname = QFileDialog.getOpenFileName(self, 'Open file', "Image files (*.jpg *.gif)")
        file_path = fname[0]
        print(file_path)
        file_path = self.set_image(label, file_path)
        self.confirmButton.setEnabled(True)
        # print(file_path)
        return(file_path)


    def Confirm(self):

        if self.count == 1:
            self.browseButton.hide()
            self.imageLabel1.show()
            self.imageLabel2.show()
            self.confirmButton.hide()
            self.compareButton.show()

        else:
            self.count += 1
            self.confirmButton.setEnabled(False)
            self.imageLabel1.hide()
            self.imageLabel2.show()

    def Compare(self):
        print("img1 = ", self.img1)
        print("img2 = ", self.img2)
        print("attach backend for comparison")
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = COMPARE()
    ex.showMaximized()
    sys.exit(app.exec_())
