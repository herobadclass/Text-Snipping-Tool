import sys
from PyQt5 import QtCore, QtGui, QtWidgets

from PIL import ImageGrab
from functools import partial
ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)

import pytesseract
import pandas.io.clipboard as pyperclip



class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super(MyWidget, self).__init__()
        self.left = QtWidgets.QApplication.desktop().geometry().left()
        self.top = QtWidgets.QApplication.desktop().geometry().top()
        self.width = QtWidgets.QApplication.desktop().geometry().width()
        self.height = QtWidgets.QApplication.desktop().geometry().height()
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.flag = False

        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()

        self.topleft = QtCore.QPoint()
        self.botright = QtCore.QPoint()

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(0.3)
        self.setStyleSheet("background-color: black;")
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.CrossCursor)

        self.show()


    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtCore.Qt.white, 2, QtCore.Qt.SolidLine, QtCore.Qt.SquareCap, QtCore.Qt.MiterJoin))
        qp.drawRect(QtCore.QRect(self.topleft, self.botright))

        frameGeometry = QtCore.QRect(QtCore.QPoint(0, 0), QtCore.QPoint(self.width, self.height))
        grabGeometry = QtCore.QRect(self.topleft, self.botright)

        region = QtGui.QRegion(frameGeometry)
        region -= QtGui.QRegion(grabGeometry)
        self.setMask(region)


    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.flag = True
            self.begin = event.pos()
            self.end = self.begin
            self.update()


    def mouseMoveEvent(self, event):
        if self.flag:
            self.end = event.pos()
            self.topleft = QtCore.QPoint(min(self.begin.x(), self.end.x()), min(self.begin.y(), self.end.y()))
            self.botright = QtCore.QPoint(max(self.begin.x(), self.end.x()), max(self.begin.y(), self.end.y()))
            self.update()


    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton & self.flag:
            self.close()

            x1 = self.topleft.x() + self.left
            y1 = self.topleft.y() + self.top
            x2 = self.botright.x() + self.left
            y2 = self.botright.y() + self.top

            img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
            # img.show()

            img_str = pytesseract.image_to_string(img)
            # print(img_str)

            pyperclip.copy(img_str)


    def keyReleaseEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()



def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MyWidget()
    window.show()
    app.exec()



if __name__ == '__main__':
   main()