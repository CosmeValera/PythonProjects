import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QMainWindow
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag

class DraggableLabel(QLabel):
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag = QDrag(self)
            mime_data = QMimeData()
            self.drag.setMimeData(mime_data)
            self.drag.exec_(Qt.MoveAction)

class DropArea(QWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        print('Something was dropped in the QWidget')
        event.accept()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.vertical_layout = QVBoxLayout(self.central_widget)

        self.horizontal_layout_1 = QHBoxLayout()
        self.horizontal_layout_2 = QHBoxLayout()

        self.label = DraggableLabel('Drag me')
        self.drop_area = DropArea()

        self.horizontal_layout_1.addWidget(self.label)
        self.horizontal_layout_2.addWidget(self.drop_area)

        self.vertical_layout.addLayout(self.horizontal_layout_1)
        self.vertical_layout.addLayout(self.horizontal_layout_2)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
