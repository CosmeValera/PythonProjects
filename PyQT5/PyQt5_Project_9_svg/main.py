import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtSvg import QSvgWidget

class SvgViewerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Load SVG file using QSvgWidget
        svg_widget = QSvgWidget('logo.svg')
        svg_widget.setFixedSize(38, 14)

        # Create layout and add QSvgWidget
        layout = QVBoxLayout(self)
        layout.addWidget(svg_widget)

        self.setLayout(layout)

        self.setGeometry(100, 100, 400, 400)
        self.setWindowTitle('SVG Viewer')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = SvgViewerApp()
    sys.exit(app.exec_())
