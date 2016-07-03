from threading import Thread
from time import sleep, time

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
        self.running = False

        self.panel = GeneralPanel(self)

        self.setWindowTitle('Simple')

        self.setGeometry(0, 0, 1400, 700)

        self.objects = []

        self.thread = Thread(target=self.run)

    def add_object(self):
        new_label = GameObject(self.canvas)
        new_label.show()
        self.canvas.update()
        self.objects.append(new_label)

    def start(self):
        print 'start'
        if self.running:
            self.thread.join()
        else:
            self.thread.start()
        self.running = not self.running

    def run(self):
        last_time = time()
        for i in range(150):
            print 'tik'
            sleep(0.02)
            delta_time = time() - last_time
            for obj in self.objects:
                obj.execute(delta_time)
                obj.update(delta_time)
            last_time = time()

    def hide_panel(self):
        for i in self.objects:
            i.panel.hide()
        self.panel.show()


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
        self.move(10, 100)

    def mousePressEvent(self, event):
        self.parent.hide_panel()


class GameObject(QLabel):
    def __init__(self, parent):
        super(GameObject, self).__init__('', parent)

        self.parent = parent
        self.setPixmap(QPixmap("./object.jpg"))
        self.resize(50, 50)
        self.setScaledContents(1)
        self.move(500, 500)
        self.vel = (0, 0)
        self.start = True

        self.panel = ControlPanel(self.parent.parent, self)

    def mousePressEvent(self, event):
        self.parent.parent.hide_panel()
        self.panel.show()

    def go(self, x, y):
        self.move(self.x() + x*1000, self.y() + y*1000)

    def execute(self, delta_time):
        if len(str(self.panel.file_path.text())) == 0:
            return
        print len(str(self.panel.file_path.text()))
        start = self.start
        execfile(str(self.panel.file_path.text()))
        self.start = False

    def update(self, delta_time):
        self.move(self.x() + self.vel[0]*delta_time, self.y() + self.vel[1]*delta_time)
        self.vel = (self.vel[0], self.vel[1]+self.parent.parent.gravity)


class GeneralPanel(QWidget):
    def __init__(self, parent):
        super(GeneralPanel, self).__init__(parent)
        self.parent = parent
        self.setGeometry(0, 0, 1000, 70)
        self.move(200, 0)
        layout = QHBoxLayout()

        self.gravity = QLineEdit("10")
        self.parent.gravity = 10
        self.gravity.setPlaceholderText("gravity:")
        self.gravity.textChanged.connect(self.on_text_changed)

        layout.addWidget(self.gravity)
        self.setLayout(layout)

    def on_text_changed(self):
        self.parent.gravity = int(str(self.gravity.text()))


class ControlPanel(QWidget):
    def __init__(self, parent, game_label):
        super(ControlPanel, self).__init__(parent)
        self.setGeometry(0, 0, 1000, 70)
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

