import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication

class PyQt5_Project_1(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("gui_app.ui", self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = PyQt5_Project_1()
    GUI.show()
    sys.exit(app.exec())