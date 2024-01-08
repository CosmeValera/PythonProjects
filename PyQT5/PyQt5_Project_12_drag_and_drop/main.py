import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit

class DragAndDrop(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Drag and drop')
        self.resize(300, 150)


def main():
    app = QApplication(sys.argv)
    demo = DragAndDrop()
    demo.show()

    print("Holaa")
    sys.exit(app.exec_())

main()