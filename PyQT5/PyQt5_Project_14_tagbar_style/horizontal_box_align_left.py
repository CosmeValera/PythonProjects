import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QFrame, QSizePolicy
from PyQt5.QtCore import Qt

class TagBar(QWidget):
    def __init__(self, parent=None):
        super(TagBar, self).__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Create a tag with text and a close button inside a QFrame
        tagFrame = QFrame(self)
        tagFrameLayout = QHBoxLayout(tagFrame)

        labelText = QLabel("Tag Text", tagFrame)
        labelText.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        closeButton = QPushButton("x", tagFrame)
        closeButton.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        closeButton.clicked.connect(tagFrame.close)

        tagFrameLayout.addWidget(labelText)
        tagFrameLayout.addWidget(closeButton)

        layout.addWidget(tagFrame, alignment=Qt.AlignLeft)

        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.initUI()

    def initUI(self):
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        # Create a horizontal layout
        layout = QHBoxLayout(centralWidget)

        # Create TagBar and QLabel, both taking 50% of space
        tagBar = TagBar(self)
        tagBar.setStyleSheet("background-color: red;")
        label = QLabel("Sample QLabel", self)

        layout.addWidget(tagBar, 1)
        layout.addWidget(label, 1)

        centralWidget.setLayout(layout)

        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle("Simple PyQt Project")
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())
