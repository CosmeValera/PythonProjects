from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget

class MyView(QWidget):
    def __init__(self):
        super().__init__()

        self.label = QLabel("Data from Model will be shown here.")
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

    def update_view(self, data):
        self.label.setText(f"Data from Model: {data}")
