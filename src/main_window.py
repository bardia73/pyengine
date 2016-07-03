from PyQt4.QtCore import QSize
from PyQt4.QtGui import *


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.canvas = Canvas(self)
        self.test_btn = QPushButton("Add Object",self)
        self.test_btn.move(10, 10)
        self.test_btn.clicked.connect(self.add_object)

        self.setWindowTitle('Simple')

        self.setGeometry(0, 0, 1400, 700)

    def add_object(self):
        new_label = GameObject(self.canvas)
        new_label.show()
        self.canvas.update()
        print new_label


class Canvas(QLabel):
    def __init__(self, parent):
        super(Canvas, self).__init__(parent)
        self.setStyleSheet("border-radius: 5px; "
                           "border: 1px solid white;"
                           "border: 2px groove white;"
                           "background-color:white;")
        self.setFrameStyle((QFrame.StyledPanel | QFrame.Plain))
        self.setGeometry(0, 0, 1380, 600)
        self.move(10, 50)


class GameObject(QLabel):
    def __init__(self, parent):
        super(GameObject, self).__init__('', parent)

        self.setPixmap(QPixmap("./object.jpg"))
        self.resize(50,50)
        self.setScaledContents(1)


        self.move(40, 40)
        print self.pos()