import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit

class DragAndDrop(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Drag and drop')
        self.resize(420, 150)
        self.initUi()

    def initUi(self):
        edit1 = QLineEdit('', self)
        edit1.setDragEnabled(True)
        edit1.move(20, 30)

        edit2 = QLineEdit('', self)
        edit2.setDragEnabled(False)
        edit2.move(20, 70)

        button = Button('&Button', self)
        button.move(290, 50)


class Button(QPushButton):
    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('text/plain'):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        print('drop event')
        self.setText(event.mimeData().text())


def main():
    app = QApplication(sys.argv)
    demo = DragAndDrop()
    demo.show()

    print("Holaa")
    sys.exit(app.exec_())

main()