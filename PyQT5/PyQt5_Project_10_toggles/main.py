import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QCheckBox, QRadioButton, QPushButton, QSlider, QToolButton

class ToggleWidgetsApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # QCheckBox example
        check_box = QCheckBox("Enable Feature")
        layout.addWidget(check_box)

        # QRadioButton example
        radio_button = QRadioButton("Option 1")
        layout.addWidget(radio_button)

        # QPushButton example
        push_button = QPushButton("Toggle State")
        layout.addWidget(push_button)

        # QSlider example
        slider = QSlider(Qt.Horizontal)  # Corrected to use Qt.Horizontal
        slider.setRange(0, 1)
        layout.addWidget(slider)

        # QToolButton example
        tool_button = QToolButton()
        tool_button.setCheckable(True)
        tool_button.setText("Toggle State")
        layout.addWidget(tool_button)

        self.setLayout(layout)

        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('Toggle Widgets App')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    a = ToggleWidgetsApp()
    sys.exit(app.exec_())
