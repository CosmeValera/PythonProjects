import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QFrame, QSizePolicy
from PyQt5.QtCore import Qt

class TagBar(QWidget):
    def __init__(self, parent=None):
        super(TagBar, self).__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout(self)

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

        # Add an invisible tagFrame to act as a placeholder
        invisibleTagFrame = QFrame(self)
        invisibleTagFrame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(invisibleTagFrame)

        # Set the background color directly on the TagBar
        self.setStyleSheet("background-color: red;")

        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.initUI()

    def initUI(self):
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        # Create a vertical layout
        layout = QVBoxLayout(centralWidget)

        # Create TagBar
        tagBar = TagBar(self)

        layout.addWidget(tagBar)

        centralWidget.setLayout(layout)

        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle("Simple PyQt Project")
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())
