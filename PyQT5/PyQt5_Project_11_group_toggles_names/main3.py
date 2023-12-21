import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QComboBox, QTreeView
from PyQt5.QtGui import QStandardItemModel, QStandardItem

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 Table, ComboBox, and TreeView Example")
        self.setGeometry(100, 100, 800, 600)


        # Create QTableWidget
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["id", "number", "name"])
        self.data = [
            {"id": "1", "number": "one", "name": "pepe"},
            {"id": "2", "number": "two", "name": "javi"},
            {"id": "3", "number": "one", "name": "javi"},
            {"id": "4", "number": "five", "name": "javi"},
            {"id": "1", "number": "four", "name": "marcos"}
        ]
        self.addItemsToTable(self.data)

        # Create QComboBox
        self.comboBox = QComboBox(self)
        self.comboBox.addItems(["", "id", "number", "name"])
        self.comboBox.currentIndexChanged.connect(self.updateTreeView)

        # Create QTreeView
        self.treeView = QTreeView(self)
        self.model = QStandardItemModel()
        self.treeView.setModel(self.model)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        layout.addWidget(self.comboBox)
        layout.addWidget(self.treeView)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def addItemsToTable(self, data):
        for row, item in enumerate(data):
            self.tableWidget.insertRow(row)
            for col, value in enumerate(item.values()):
                self.tableWidget.setItem(row, col, QTableWidgetItem(str(value)))

    def updateTreeView(self, index):
        header = self.comboBox.currentText()
        self.model.clear()
        root_item = self.model.invisibleRootItem()

        grouped_data = {}
        for row in range(self.tableWidget.rowCount()):
            key = self.tableWidget.item(row, self.comboBox.currentIndex()).text()
            if key not in grouped_data:
                grouped_data[key] = []
            grouped_data[key].append([self.tableWidget.item(row, col).text() for col in range(3)])

        for key, values in grouped_data.items():
            category_item = QStandardItem(key)
            for v in values:
                row_item = QStandardItem(", ".join(v))  # Combine values into a single string
                category_item.appendRow(row_item)
            root_item.appendRow(category_item)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())