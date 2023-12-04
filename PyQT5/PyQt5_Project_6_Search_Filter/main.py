import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QListWidget, QLabel, QPushButton
from PyQt5.QtGui import QFont
from qtawesome import icon

class DataFilterApp(QWidget):
    def __init__(self):
        super().__init__()

        self.data = ["Apple", "Banana", "Orange", "Grapes", "Cherry", "Strawberry", "Blueberry", "Raspberry"]
        self.filtered_data = self.data.copy()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.filter_input = QLineEdit(self)
        self.filter_input.setPlaceholderText("Type to filter...")

        # Set font for the filter input
        font = QFont()
        font.setBold(True)
        self.filter_input.setFont(font)

        # Add clear button to the filter input
        self.filter_input.setClearButtonEnabled(True)

        # Add a search icon from FontAwesome to the filter input
        search_icon = icon('fa.search', color='black')
        self.filter_input.addAction(search_icon, QLineEdit.LeadingPosition)

        # Connect the filter signal to the update_filter method
        self.filter_input.textChanged.connect(self.update_filter)

        self.data_list = QListWidget(self)
        self.update_data_list()

        layout.addWidget(QLabel("Filter:"))
        layout.addWidget(self.filter_input)
        layout.addWidget(QLabel("Filtered Data:"))
        layout.addWidget(self.data_list)

        self.setLayout(layout)

        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('Data Filter App')
        self.show()

    def update_data_list(self):
        self.data_list.clear()
        self.data_list.addItems(self.filtered_data)

    def update_filter(self, text):
        self.filtered_data = [item for item in self.data if text.lower() in item.lower()]
        self.update_data_list()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DataFilterApp()
    sys.exit(app.exec_())
