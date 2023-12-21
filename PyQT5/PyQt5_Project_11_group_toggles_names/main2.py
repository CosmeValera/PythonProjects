import sys
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton

class GroupedTableWidget(QWidget):
    def __init__(self):
        super(GroupedTableWidget, self).__init__()

        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(["id", "number", "name"])

        self.data = [
            {"id": "1", "number": "one", "name": "pepe"},
            {"id": "2", "number": "two", "name": "javi"},
            {"id": "3", "number": "three", "name": "javi"}
        ]

        self.populate_table()

        self.group_button = QPushButton("Toggle Group")
        self.group_button.clicked.connect(self.toggle_group)

        layout = QVBoxLayout(self)
        layout.addWidget(self.table_widget)
        layout.addWidget(self.group_button)

    def populate_table(self):
        self.table_widget.setRowCount(len(self.data))

        for row, item in enumerate(self.data):
            for col, value in enumerate(item.values()):
                self.table_widget.setItem(row, col, QTableWidgetItem(value))

    def toggle_group(self):
        group_name = "pepe"  # Replace with the desired group name
        show_group = not self.is_group_visible(group_name)

        for row in range(self.table_widget.rowCount()):
            name_item = self.table_widget.item(row, 2)  # Assuming "name" is the third column
            if name_item.text() == group_name:
                self.table_widget.setRowHidden(row, not show_group)

    def is_group_visible(self, group_name):
        for row in range(self.table_widget.rowCount()):
            name_item = self.table_widget.item(row, 2)  # Assuming "name" is the third column
            if name_item.text() == group_name and not self.table_widget.isRowHidden(row):
                return True
        return False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GroupedTableWidget()
    window.show()
    sys.exit(app.exec_())
