
import sys
from PyQt4.QtGui import *

from src import MainWindow


def main():

    app = QApplication(sys.argv)

    win = MainWindow()
    win.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

