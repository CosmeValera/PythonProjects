import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QToolButton
from PyQt5.QtGui import QIcon, QPainterPath, QRegion
from PyQt5.QtCore import Qt, QRectF

class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        title_bar_layout = QHBoxLayout(self)
        title_bar_layout.setContentsMargins(0, 0, 0, 0)

        self.title = QLabel(f"{self.__class__.__name__}", self)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title_bar_layout.addWidget(self.title)

        # Icons layout
        icons_layout = QHBoxLayout()
        icons_layout.setContentsMargins(0, 0, 0, 0)

        # Minimize button
        self.minimize_button = QToolButton(self)
        self.minimize_button.setIcon(parent.style().standardIcon(QApplication.style().SP_TitleBarMinButton))
        self.minimize_button.clicked.connect(parent.showMinimized)

        # Maximize button
        self.maximize_button = QToolButton(self)
        self.maximize_button.setIcon(parent.style().standardIcon(QApplication.style().SP_TitleBarMaxButton))
        self.maximize_button.clicked.connect(self.toggle_maximized)

        # Close button
        self.close_button = QToolButton(self)
        self.close_button.setIcon(parent.style().standardIcon(QApplication.style().SP_TitleBarCloseButton))
        self.close_button.clicked.connect(parent.close)

        icons_layout.addWidget(self.minimize_button)
        icons_layout.addWidget(self.maximize_button)
        icons_layout.addWidget(self.close_button)

        title_bar_layout.addLayout(icons_layout)

        # Set the title bar color to pink and fix the height
        self.setStyleSheet("background-color: pink;")
        self.setFixedHeight(32)

    def toggle_maximized(self):
        if self.window().isMaximized():
            self.window().showNormal()
        else:
            self.window().showMaximized()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Custom Title Bar")
        self.resize(400, 200)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Set rounded borders
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), 10, 10)
        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)

        central_widget = QWidget()
        central_widget.setStyleSheet("background: white;")

        self.title_bar = CustomTitleBar(self)

        work_space_layout = QVBoxLayout()
        work_space_layout.setContentsMargins(11, 11, 11, 11)
        work_space_layout.addWidget(QLabel("Hello, World!", self))

        central_layout = QVBoxLayout(central_widget)
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.addWidget(self.title_bar)
        central_layout.addLayout(work_space_layout)

        self.setCentralWidget(central_widget)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_position = event.globalPos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if hasattr(self, 'drag_start_position'):
            delta = event.globalPos() - self.drag_start_position
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.drag_start_position = event.globalPos()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if hasattr(self, 'drag_start_position'):
            delattr(self, 'drag_start_position')
        super().mouseReleaseEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
