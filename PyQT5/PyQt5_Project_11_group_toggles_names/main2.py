import sys
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QComboBox

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

        self.column_selector = QComboBox(self)
        self.column_selector.addItems(["id", "number", "name"])
        self.column_selector.currentIndexChanged.connect(self.group_by_column)

        layout = QVBoxLayout(self)
        layout.addWidget(self.column_selector)
        layout.addWidget(self.table_widget)

    def populate_table(self):
        self.table_widget.setRowCount(len(self.data))

        for row, item in enumerate(self.data):
            for col, value in enumerate(item.values()):
                self.table_widget.setItem(row, col, QTableWidgetItem(value))

    def group_by_column(self, index):
        column_name = self.column_selector.itemText(index)

        if column_name == "name":
            self.group_by_name()

    def group_by_name(self):
        name_column_index = 2  # Assuming "name" is the third column

        grouped_data = {}
        for row in range(self.table_widget.rowCount()):
            name_item = self.table_widget.item(row, name_column_index)

            name_value = name_item.text()
            if name_value not in grouped_data:
                grouped_data[name_value] = {"id": set(), "number": set()}

            id_item = self.table_widget.item(row, 0)  # Assuming "id" is the first column
            number_item = self.table_widget.item(row, 1)  # Assuming "number" is the second column

            grouped_data[name_value]["id"].add(id_item.text())
            grouped_data[name_value]["number"].add(number_item.text())

        # Clear the table
        self.table_widget.setRowCount(0)

        # Add grouped data to the table
        for name_value, columns in grouped_data.items():
            self.table_widget.insertRow(self.table_widget.rowCount())

            id_text = ", ".join(sorted(columns["id"]))
            number_text = ", ".join(sorted(columns["number"]))

            self.table_widget.setItem(self.table_widget.rowCount() - 1, 0, QTableWidgetItem(id_text))
            self.table_widget.setItem(self.table_widget.rowCount() - 1, 1, QTableWidgetItem(number_text))
            self.table_widget.setItem(self.table_widget.rowCount() - 1, 2, QTableWidgetItem(name_value))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GroupedTableWidget()
    window.show()
    sys.exit(app.exec_())
