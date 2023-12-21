import sys
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QComboBox

class GroupedTableWidget(QWidget):
    def __init__(self):
        super(GroupedTableWidget, self).__init__()

        self.original_data = [
            {"id": "1", "number": "one", "name": "pepe"},
            {"id": "2", "number": "two", "name": "javi"},
            {"id": "3", "number": "one", "name": "javi"},
            {"id": "4", "number": "five", "name": "javi"},
            {"id": "1", "number": "four", "name": "marcos"}
        ]

        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(["id", "number", "name"])

        self.populate_table()

        self.column_selector = QComboBox(self)
        self.column_selector.addItems(["", "id", "number", "name"])
        self.column_selector.currentIndexChanged.connect(self.group_by_column)

        layout = QVBoxLayout(self)
        layout.addWidget(self.column_selector)
        layout.addWidget(self.table_widget)

    def populate_table(self):
        self.table_widget.setRowCount(len(self.original_data))

        for row, item in enumerate(self.original_data):
            for col, value in enumerate(item.values()):
                self.table_widget.setItem(row, col, QTableWidgetItem(value))

    def group_by_column(self, index):
        column_name = self.column_selector.itemText(index)

        self.restore_original_data()
        if column_name in {"id", "name", "number"}:
            self.group_by_column_value(column_name)

    def group_by_column_value(self, column_name):
        column_index = {"id": 0, "number": 1, "name": 2}[column_name]

        grouped_data = {}
        for row in range(self.table_widget.rowCount()):
            column_item = self.table_widget.item(row, column_index)

            column_value = column_item.text()
            if column_value not in grouped_data:
                grouped_data[column_value] = {"id": set(), "number": set(), "name": set()}

            for col in range(self.table_widget.columnCount()):
                value = self.table_widget.item(row, col).text()
                grouped_data[column_value][self.table_widget.horizontalHeaderItem(col).text()].add(value)

        # Clear the table
        self.table_widget.setRowCount(0)

        # Add grouped data to the table
        for column_value, columns in grouped_data.items():
            self.table_widget.insertRow(self.table_widget.rowCount())

            for col, values in enumerate(columns.values()):
                text = ", ".join(sorted(values))
                self.table_widget.setItem(self.table_widget.rowCount() - 1, col, QTableWidgetItem(text))

    def restore_original_data(self):
        self.table_widget.setRowCount(0)
        for row, item in enumerate(self.original_data):
            self.table_widget.insertRow(row)
            for col, value in enumerate(item.values()):
                self.table_widget.setItem(row, col, QTableWidgetItem(value))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GroupedTableWidget()
    window.show()
    sys.exit(app.exec_())
