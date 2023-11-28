import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication

class PyQt5_Project_1(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("gui_app.ui", self)
        self.disableBut.setEnabled(False)
        self.enableBut.clicked.connect(self.enable)
        self.disableBut.clicked.connect(self.disable)

    def enable(self):
        self.enableBut.setEnabled(False)
        self.disableBut.setEnabled(True)
        self.enableLab.setText("Enabled")

    def disable(self):
        self.enableBut.setEnabled(True)
        self.disableBut.setEnabled(False)
        self.enableLab.setText("Disabled")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = PyQt5_Project_1()
    GUI.show()
    sys.exit(app.exec())