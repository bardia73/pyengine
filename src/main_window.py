from PyQt4.QtCore import *
from PyQt4.QtGui import *


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.canvas = Canvas(self)
        self.test_btn = QPushButton("Add Object", self)
        self.test_btn.move(10, 10)
        self.test_btn.clicked.connect(self.add_object)

        self.setWindowTitle('Simple')

        self.setGeometry(0, 0, 1400, 700)

        self.objects = []

    def add_object(self):
        new_label = GameObject(self.canvas)
        new_label.show()
        self.canvas.update()
        self.objects.append(new_label)

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
        print 'fuck'
        self.panel.show()


class ControlPanel(QWidget):
    def __init__(self, parent, game_label):
        super(ControlPanel, self).__init__(parent)
        self.setGeometry(0, 0, 1000, 50)
        self.move(100, 10)
        self.game_label = game_label
        layout = QHBoxLayout()

        self.file_path = QLineEdit()
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
        self.game_label.move(int(self.x_val.text()),int(self.y_val.text()))