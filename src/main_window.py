from threading import Thread
from time import sleep

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.canvas = Canvas(self)
        self.test_btn = QPushButton("Add Object", self)
        self.run_btn = QPushButton("RUN", self)
        self.test_btn.move(10, 10)
        self.run_btn.move(100, 10)
        self.test_btn.clicked.connect(self.add_object)
        self.run_btn.clicked.connect(self.start)

        self.setWindowTitle('Simple')

        self.setGeometry(0, 0, 1400, 700)

        self.objects = []

    def add_object(self):
        new_label = GameObject(self.canvas)
        new_label.show()
        self.canvas.update()
        self.objects.append(new_label)

    def start(self):
        print 'start'
        t = Thread(target=self.run)
        t.start()

    def run(self):
        for i in range(1500):
            print 'tik'
            sleep(0.002)
            for obj in self.objects:
                obj.execute()

    def hide_panel(self):
        for i in self.objects:
            i.panel.hide()


class Canvas(QLabel):
    def __init__(self, parent):
        super(Canvas, self).__init__(parent)
        self.parent = parent
        self.setStyleSheet("border-radius: 5px; "
                           "border: 1px solid white;"
                           "border: 2px groove white;"
                           "background-color:white;")
        self.setFrameStyle((QFrame.StyledPanel | QFrame.Plain))
        self.setGeometry(0, 0, 1380, 600)
        self.move(10, 50)

    def mousePressEvent(self, event):
        self.parent.hide_panel()


class GameObject(QLabel):
    def __init__(self, parent):
        super(GameObject, self).__init__('', parent)

        self.parent = parent
        self.setPixmap(QPixmap("./object.jpg"))
        self.resize(50, 50)
        self.setScaledContents(1)
        self.move(40, 40)

        self.panel = ControlPanel(self.parent.parent, self)

    def mousePressEvent(self, event):
        self.parent.parent.hide_panel()
        self.panel.show()

    def moveRight(self):
        self.move(self.x() + 1, self.y())

    def moveDown(self):
        self.move(self.x(), self.y() + 1)

    def moveLeft(self):
        self.move(self.x() - 1, self.y())

    def moveUp(self):
        self.move(self.x(), self.y() - 1)

    def execute(self):
        if len(str(self.panel.file_path.text())) == 0:
            return
        print len(str(self.panel.file_path.text()))
        execfile(str(self.panel.file_path.text()))


class ControlPanel(QWidget):
    def __init__(self, parent, game_label):
        super(ControlPanel, self).__init__(parent)
        self.setGeometry(0, 0, 1000, 50)
        self.move(200, 0)
        self.game_label = game_label
        layout = QHBoxLayout()

        self.file_path = QLineEdit("./obj1.py")
        self.x_val = QLineEdit("10")
        self.x_val.setPlaceholderText("X:")
        self.x_val.textChanged.connect(self.on_text_changed)
        self.y_val = QLineEdit("10")
        self.y_val.setPlaceholderText("Y:")
        self.y_val.textChanged.connect(self.on_text_changed)

        layout.addWidget(self.file_path)
        layout.addWidget(self.x_val)
        layout.addWidget(self.y_val)
        self.setLayout(layout)

    def on_text_changed(self):
        self.game_label.move(int(self.x_val.text()), int(self.y_val.text()))
