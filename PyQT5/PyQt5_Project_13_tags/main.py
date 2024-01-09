import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag, QPixmap

class DraggableLineEdit(QLineEdit):
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText(self.text())
            drag.setMimeData(mime_data)
            pixmap = QPixmap(self.size())
            self.render(pixmap)
            drag.setPixmap(pixmap)
            drag.setHotSpot(event.pos() - self.rect().topLeft())
            drag.exec_(Qt.MoveAction)

class DropLabel(QLabel):
    def __init__(self, title):
        super().__init__(title)
        self.setAlignment(Qt.AlignCenter)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        self.setText(event.mimeData().text())

class DragAndDropApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Create draggable lines
        line1 = DraggableLineEdit("Drag me!")
        line2 = DraggableLineEdit("Drag me too!")

        # Create drop labels
        label1 = DropLabel("Drop here")
        label2 = DropLabel("Drop here")
        label3 = DropLabel("Drop here")

        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(line1)
        layout.addWidget(line2)
        layout.addWidget(label1)
        layout.addWidget(label2)
        layout.addWidget(label3)

        # Set the main layout for the window
        self.setLayout(layout)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Drag and Drop Example')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DragAndDropApp()
    sys.exit(app.exec_())
