from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import qpageview
import sys
import os
from ICM_test2 import *


class dropImageLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setText("\n\n Drop Image Here \n\n")
        self.setStyleSheet("border: 4px dashed grey")

    def setPixmap(self, image):
        super().setPixmap(image)


class ImageLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)

    def setPixmap(self, image):
        super().setPixmap(image)


class imgdrop1(QWidget):
    def __init__(self):

        self.img1 = ""  # path for image 1
        self.img2 = ""  # path for image 2
        self.count = 0

        super().__init__()
        self.setWindowTitle("Drop Images")
        self.resize(800, 500)

        self.setAcceptDrops(True)

        self.pccoelogo = ImageLabel()
        self.set_image(self.pccoelogo, "logo/PCCoELOGO.png")

        self.companylogo = ImageLabel()
        self.set_image(self.companylogo, "logo/CompanyLOGO.png")

        # self.companyname = QLabel()
        # self.companyname.setText("Sigma")
        # self.companyname.resize(600, 50)

        self.imageLabel1 = dropImageLabel()
        self.imageLabel2 = dropImageLabel()
        self.imageLabel2.hide()

        layout1 = QVBoxLayout()
        layout2 = QHBoxLayout()

        layout2.addWidget(self.pccoelogo)
        # layout2.addWidget(self.companyname)
        layout2.addWidget(self.companylogo)

        layout1.addLayout(layout2)

        layout1.addWidget(self.imageLabel1)
        self.imageLabel1.setText("\n\n Drop Original Image Here \n\n")

        layout1.addWidget(self.imageLabel2)
        self.imageLabel2.setText("\n\n Drop Created Image Here \n\n")
        self.imageLabel2.hide()

        self.confirmButton = QPushButton("Confirm")
        layout1.addWidget(self.confirmButton, 1)
        self.confirmButton.setEnabled(False)

        self.compareButton = QPushButton("Compare")
        layout1.addWidget(self.compareButton, 1)
        self.compareButton.hide()

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

            if (
                os.path.splitext(file_path)[-1].lower() == ".png"
                or os.path.splitext(file_path)[-1].lower() == ".jpeg"
                or os.path.splitext(file_path)[-1].lower() == ".jpg"
            ):
                if self.count == 1:
                    self.set_image(self.imageLabel2, file_path)
                    self.img2 = file_path
                elif self.count == 0:
                    self.set_image(self.imageLabel1, file_path)
                    self.img1 = file_path

            elif os.path.splitext(file_path)[-1].lower() == ".pdf":
                if self.count == 1:
                    self.imageLabel2.setText(
                        "\n\n PDF preview is unavailable. \n Filepath: "
                        + file_path
                        + "\n"
                    )
                    self.img2 = file_path
                else:
                    self.imageLabel1.setText(
                        "\n\n PDF preview is unavailable. \n Filepath: "
                        + file_path
                        + "\n"
                    )
                    self.img1 = file_path
                self.set_pdf(file_path)
                print("connect to pdf2image class")
                # self.close()

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
            self.confirmButton.clicked.connect(self.Confirm)

            event.accept()

        else:
            event.Ignore()

    def set_image(self, label, file_path):
        label.setPixmap(QPixmap(file_path))

    def set_pdf(self, file_path):
        v = qpageview.View()
        v.show()
        v.loadPdf(file_path)

    def Confirm(self):

        if self.count == 1:
            self.imageLabel1.show()
            self.confirmButton.hide()
            self.compareButton.show()
            self.compareButton.clicked.connect(self.Compare)

        else:
            self.count += 1
            self.confirmButton.setEnabled(False)
            self.imageLabel1.hide()
            self.imageLabel2.show()

    def Compare(self):
        print("1")
        print("img1 = ", self.img1)
        print("img2 = ", self.img2)
        print("attach backend for comparison")

        img1 = ImageObj(self.img1)
        img2 = ImageObj(self.img2)
        cordinates = testImageBlock2(img1, img2)
        # All diff in one image
        inOne(cordinates, img1.img, img2.img)
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = imgdrop1()
    ex.show()
    sys.exit(app.exec_())
