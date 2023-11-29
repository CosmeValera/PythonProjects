from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget
from qt_material import apply_stylesheet

class MyView(QWidget):
    def __init__(self):
        super().__init__()

        # Apply the Qt Material theme
        apply_stylesheet(self, theme='dark_teal.xml')

        self.label = QLabel("Data from Model will be shown here.")
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

    def update_view(self, data):
        self.label.setText(f"Data from Model: {data}")
