from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont

def main():
    app = QApplication([])
    window = QWidget()
    window.setGeometry(100, 100, 200, 300)
    window.setWindowTitle("My simple GUI")

    layout = QVBoxLayout()

    label = QLabel("Press the button below")
    button = QPushButton("Press me !")

    layout.addWidget(label)
    layout.addWidget(button)
    

    window.show()
    app.exec_()

if __name__ == '__main__':
    main()