from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from pdf2image import convert_from_path
import sys
import os

class Home(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Home")
        windowSize = str(self.size())
        self.windowDimensions = list(map(int, windowSize.split("(")[1].split(")")[0].split(", ")))
        self.setupUi()

    def setupUi(self):
        self.header = QFrame()
        self.header.setFixedHeight(int(self.windowDimensions[1]/3.5))
        self.header.setGeometry(QRect(0, 0, self.windowDimensions[0], 0))
        self.header.setAutoFillBackground(False)
        self.header.setStyleSheet("background-color: #E7EFF3;")
        self.header.setFrameShape(QFrame.StyledPanel)
        self.header.setFrameShadow(QFrame.Raised)
        
        self.appNameLabel = QLabel(self.header)
        font = QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(30)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.appNameLabel.setFont(font)
        self.appNameLabel.setText("\"PYCOM\" - 2D Drawing Comparison")
        self.appNameLabel.setGeometry(QRect(20,10, 1000, 71))
        
        self.homeMenuBtn = QPushButton("Home", self.header)
        self.homeMenuBtn.setGeometry(10, int(((str(self.header.mapToGlobal(self.header.geometry().bottomLeft())).split(','))[1])[1:-1])-30, 100, 30)
        font = QFont()
        font.setPointSize(11)
        self.homeMenuBtn.setFont(font)
        self.homeMenuBtn.setStyleSheet("background-color: #8EA6B4")
        
        self.compareMenuBtn = QPushButton("Compare", self.header)
        self.compareMenuBtn.setGeometry(120, int(((str(self.header.mapToGlobal(self.header.geometry().bottomLeft())).split(','))[1])[1:-1])-30, 120, 30)
        font.setPointSize(11)
        self.compareMenuBtn.setFont(font)
        self.compareMenuBtn.setStyleSheet("color: black; background-color: #8EA6B4")
        self.compareMenuBtn.clicked.connect(lambda: openWin(Compare(), self))
        
        # self.aboutMenuBtn = QPushButton("About Us", self.header)
        # self.aboutMenuBtn.setGeometry(250, int(((str(self.header.mapToGlobal(self.header.geometry().bottomLeft())).split(','))[1])[1:-1])-30, 120, 30)
        # font.setPointSize(11)
        # self.aboutMenuBtn.setFont(font)
        # self.aboutMenuBtn.setStyleSheet("background-color: #8EA6B4")

        self.pccoeLogo = QLabel(self.header)
        self.pccoeLogo.setGeometry(QRect(1730, 5, 150, 120))
        self.pccoeLogo.setText("")
        self.pccoeLogo.setPixmap(QPixmap("imageComparison/logo/PCCoELOGO.png"))
        self.pccoeLogo.setScaledContents(True)

        self.body1 = QFrame()
        self.body1.setStyleSheet("background-color: #F4F9F9;")
        self.body1.setFrameShape(QFrame.StyledPanel)
        self.body1.setFrameShadow(QFrame.Raised)

        self.aboutLabel = QLabel(self.body1)
        self.aboutLabel.setGeometry(QRect(1550, 10, 350, 20))
        font.setPointSize(10)
        font.setItalic(True)
        self.aboutLabel.setFont(font)
        self.aboutLabel.setText("* Contact us at swati.chandurkar@gmail.com")

        self.descLabel1 = QLabel(self.body1)
        self.descLabel1.setGeometry(QRect(30, 40, 1700, 60))
        font.setFamily("aakar")
        font.setPointSize(22)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.descLabel1.setFont(font)
        self.descLabel1.setText("\"Where You can View, Measure, Section, Analyze, Compare, and Export CAD Files !\"")

        self.descLabel2 = QLabel(self.body1)
        self.descLabel2.setGeometry(QRect(30, 120, 1500, 700))
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.descLabel2.setFont(font)
        self.descLabel2.setText("This Automation software is a CAD tool to convert 2D CAD Parts and Assembly files to 2D PDF.\n"
                                "Schedule tasks to convert CAD files automatically. Save on CAD licenses for CAD file conversion and\n"
                                "export PDF files."
                                "Start Your CAD drawings comparision :\n"
                                " - Easily view popular 2D CAD files in one application\n"
                                " - No training required\n"
                                " - Supports all major CAD softwares\n\n"
                                "Take accurate measurements, cut dynamic sections, analyze components, compare revisions and export to PDF format.\n\n"
                                "The Automation software tool will quickly identify changes to revisions or versions of CAD drawings with the ability\n"
                                " to visually compare 2D drawing files. Comparing 2D files can save a lot of time and speed up collaboration.\n\n"
                                "A typical 2D drawing is modified many times during the design cycle and also several times during subsequent series\n"
                                "production. Whether the changes are small or large, it usually takes a long time to learn from these changes. Visual\n"
                                "comparison of CAD models and drawings is easy to find even for novice users and since the solution is automatic,\n"
                                "it is a huge time saver if done manually. Added comparison tool to the software to quickly compare two CAD drawings. \n\n"
                                "The comparison helps identify the following changes:\n"
                                "1. Addition, deletion and modification of views\n"
                                "2. Changes to the geometry of the model\n\n"
                                "This tool works for Catia drawings (.CATDrawing) and 2D PDF drawings.")

        self.sampleImg = QLabel(self.body1)
        self.sampleImg.setGeometry(QRect(1250, 150, 640, 350))
        self.sampleImg.setText("")
        self.sampleImg.setPixmap(QPixmap("outputSS.png"))
        self.sampleImg.setScaledContents(True)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.header)
        mainLayout.addWidget(self.body1)

        self.setLayout(mainLayout)
        # print(self.children)

class Compare(QWidget):
    def __init__(self):
        Home().close()
        self.img1 = ""  # path for image 1
        self.img2 = ""  # path for image 2
        self.count = 1
        

        super().__init__()
        self.setWindowTitle("Compare")
        windowSize = str(self.size())
        self.windowDimensions = list(map(int, windowSize.split("(")[1].split(")")[0].split(", ")))
        self.setAcceptDrops(True)
        self.setupUi()

    def setupUi(self):

        self.header = QFrame()
        self.header.setFixedHeight(int(self.windowDimensions[1]/3.5))
        self.header.setGeometry(QRect(0, 0, self.windowDimensions[0], 0))
        self.header.setAutoFillBackground(False)
        self.header.setStyleSheet("background-color: #E7EFF3;")
        self.header.setFrameShape(QFrame.StyledPanel)
        self.header.setFrameShadow(QFrame.Raised)
        
        self.appNameLabel = QLabel(self.header)
        font = QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(30)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.appNameLabel.setFont(font)
        self.appNameLabel.setText("\"PYCOM\" - 2D Drawing Comparison")
        self.appNameLabel.setGeometry(QRect(20,10, 1000, 71))
        
        self.homeMenuBtn = QPushButton("Home", self.header)
        self.homeMenuBtn.setGeometry(10, int(((str(self.header.mapToGlobal(self.header.geometry().bottomLeft())).split(','))[1])[1:-1])-30, 100, 30)
        font = QFont()
        font.setPointSize(11)
        self.homeMenuBtn.setFont(font)
        self.homeMenuBtn.setStyleSheet("background-color: #8EA6B4")
        self.homeMenuBtn.clicked.connect(lambda: openWin(Home(), self))
        
        self.compareMenuBtn = QPushButton("Compare", self.header)
        self.compareMenuBtn.setGeometry(120, int(((str(self.header.mapToGlobal(self.header.geometry().bottomLeft())).split(','))[1])[1:-1])-30, 120, 30)
        font.setPointSize(11)
        self.compareMenuBtn.setFont(font)
        self.compareMenuBtn.setStyleSheet("color: black; background-color: #8EA6B4")
        
        # self.aboutMenuBtn = QPushButton("About Us", self.header)
        # self.aboutMenuBtn.setGeometry(250, int(((str(self.header.mapToGlobal(self.header.geometry().bottomLeft())).split(','))[1])[1:-1])-30, 120, 30)
        # font.setPointSize(11)
        # self.aboutMenuBtn.setFont(font)
        # self.aboutMenuBtn.setStyleSheet("background-color: #8EA6B4")

        self.pccoeLogo = QLabel(self.header)
        self.pccoeLogo.setGeometry(QRect(1730, 5, 150, 120))
        self.pccoeLogo.setText("")
        self.pccoeLogo.setPixmap(QPixmap("imageComparison/logo/PCCoELOGO.png"))
        self.pccoeLogo.setScaledContents(True)

        self.body1 = QFrame()
        self.body1.setStyleSheet("background-color: #F4F9F9;")
        self.body1.setFrameShape(QFrame.StyledPanel)
        self.body1.setFrameShadow(QFrame.Raised)

        self.aboutLabel = QLabel(self.body1)
        self.aboutLabel.setGeometry(QRect(1550, 10, 350, 20))
        font.setPointSize(10)
        font.setItalic(True)
        self.aboutLabel.setFont(font)
        self.aboutLabel.setText("* Contact us at swati.chandurkar@gmail.com")

        self.descLabel1 = QLabel(self.body1)
        self.descLabel1.setGeometry(QRect(30, 60, 650, 30))
        font.setFamily("aakar")
        font.setPointSize(16)
        font.setItalic(True)
        self.descLabel1.setFont(font)
        self.descLabel1.setText("Here are the steps to compare 2D drawing files :")

        self.descLabel2 = QLabel(self.body1)
        self.descLabel2.setGeometry(QRect(30, 115, 650, 150))
        font.setPointSize(14)
        font.setItalic(True)
        self.descLabel2.setFont(font)
        self.descLabel2.setText("1. Click Browse and select file (jpg or pdf) to be added\n"
                                "2. Add both drawings to the two fields below\n"
                                "3. Click the Compare Button\n"
                                "4. Comparision output is ready in PDF form\n")

        self.descLabel3 = QLabel(self.body1)
        self.descLabel3.setGeometry(QRect(1000, 60, 700, 55))
        font.setPointSize(16)
        font.setItalic(True)
        self.descLabel3.setFont(font)
        self.descLabel3.setText("The results are computed and shown with the following:\n")

        self.descLabel4 = QLabel(self.body1)
        self.descLabel4.setGeometry(QRect(1000, 115, 700, 85))
        font.setPointSize(14)
        font.setItalic(True)
        self.descLabel4.setFont(font)
        self.descLabel4.setText("1. New views, dimensions or information is shown in RED color\n"
                                "2. Removed Views, dimensions and are shown in red color\n"
                                "3. All unchanged drawing elements are shown in default color")
        
        self.ComparePushBtn = QPushButton(self.body1)
        self.ComparePushBtn.setGeometry(QRect(750, 300, 400, 50))
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.ComparePushBtn.setFont(font)
        self.ComparePushBtn.setText("Click here to Compare")
        self.ComparePushBtn.setStyleSheet("background-color: #CCF2F4")
        self.ComparePushBtn.clicked.connect(lambda: self.Compare())
        self.ComparePushBtn.setEnabled(True)

        body2 = QHBoxLayout()
        imageLayout1 = QVBoxLayout()
        imageLayout2 = QVBoxLayout()

        self.dropImgLabel1 = QLabel()
        self.dropImgLabel1.setAlignment(Qt.AlignCenter)
        self.dropImgLabel1.setText("\n\nDrawing 1\n\n")
        self.dropImgLabel1.setStyleSheet("border: 4px dashed grey")
        self.dropImgLabel1.setFixedHeight(400)
        self.dropImgLabel1.setScaledContents(True)
        
        self.browse1 = QPushButton("Browse for Drawing 1")
        self.browse1.clicked.connect(lambda: self.getImage(self.dropImgLabel1))

        imageLayout1.addWidget(self.dropImgLabel1)
        imageLayout1.addWidget(self.browse1)

        self.dropImgLabel2 = QLabel()
        self.dropImgLabel2.setAlignment(Qt.AlignCenter)
        self.dropImgLabel2.setText("\n\n Drawing 2\n\n")
        self.dropImgLabel2.setStyleSheet("border: 4px dashed grey")
        self.dropImgLabel2.setFixedHeight(400)
        self.dropImgLabel2.setScaledContents(True)

        self.browse2 = QPushButton("Browse for Drawing 2")
        self.browse2.clicked.connect(lambda: self.getImage(self.dropImgLabel2))

        imageLayout2.addWidget(self.dropImgLabel2)
        imageLayout2.addWidget(self.browse2)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.header)
        mainLayout.addWidget(self.body1)
        body2.addLayout(imageLayout1)
        body2.addLayout(imageLayout2)
        mainLayout.addLayout(body2)
        

        self.setLayout(mainLayout)
        # print(self.children)

    def getImage(self, label):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'c\\', "All files (*.*)")
        file_path = fname[0]
        # print("getImage", self, file_path)
        file_path = self.set_image(label, file_path)
    
    def set_image(self, label, file_path):
        # print("set_image method: ", label, file_path)
        if os.path.splitext(file_path)[-1].lower() == ".pdf":
            file_path = self.convertPDF2JPG(file_path, label)

        if QPixmap(file_path) is not None:
            imageWidth, imageHeight = QPixmap(file_path).width(), QPixmap(file_path).height()
            labelWidth, labelHeight = label.width(), label.height()
            ratio = min(labelWidth / imageWidth, labelHeight / imageHeight)
            newWidth = int(imageWidth * ratio)
            newPixmap = QPixmap(file_path).scaledToWidth(newWidth, Qt.TransformationMode.FastTransformation)
            label.setPixmap(newPixmap)
            self.setFilePath(file_path, label)
            return(file_path)

    def setFilePath(self, file_path, label):
        # print("setFilePath method")
        if label == self.dropImgLabel1:
            self.img1 = file_path
            # print("img1=", self.img1)
        elif label == self.dropImgLabel2:
            self.img2 = file_path
            # print("img2=", self.img2)
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

    def convertPDF2JPG(self, file_path, label):
        # print("convertPDF2JPG method")
        if label == self.dropImgLabel1:
            savename = "img1"
        else:
            savename = "img2"

        images = convert_from_path(file_path)
        for i in range(len(images)):
            new_file_path = "industrySample/" + savename + str(self.count) + ".jpg"
            images[i].save(new_file_path, "JPEG")
            return(new_file_path)

    def Compare(self):
        if self.img1 == '' or self.img2 == '':
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText(
                "One or both of the drawings is not uploaded. Please try again."
            )
            msg.setWindowTitle("Error")
            msg.addButton(QMessageBox.Ok)
            msg.exec_()
        # print("Compare Method")
        print("img1 = ", self.img1)
        print("img2 = ", self.img2)
        print("attach backend for comparison")
        # delete file created when pdf to jpeg -> os.delete("<filepath")
        self.close()

def openWin(win, current = None):
    if current != None:
        current.close()
    win.showMaximized()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    openWin(Home())
    sys.exit(app.exec_())
