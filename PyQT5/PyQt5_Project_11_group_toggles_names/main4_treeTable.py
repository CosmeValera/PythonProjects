import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget

class TreeTable(QTreeWidget):
    def __init__(self):
        super().__init__()
        data = [
            ('1', 'Category 1', [('1.1', 'Item 1.1', [('1.1.1', 'Subitem 1.1.1')])]),
            ('2', 'Category 2', [('2.1', 'Item 2.1'), ('2.2', 'Item 2.2')]),
        ]
        headers = ['Id', 'Name']

        self.setColumnCount(len(headers))
        self.setHeaderLabels(headers)
        self.addItemsRecursively(self, data)

        # Connect the itemClicked signal to the custom method
        self.itemClicked.connect(self.on_item_clicked)

    def addItemsRecursively(self, parent, items):
        for item in items:
            currentItem = QTreeWidgetItem(parent, item[:2])
            if len(item) > 2:
                self.addItemsRecursively(currentItem, item[2])

    def on_item_clicked(self, item, column):
        # Check if the clicked item has values
        if item.childCount() == 0:
            # Extract values from the clicked item
            values = [item.text(column) for column in range(self.columnCount())]
            print("Clicked Item Values:", values)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle("TreeTable Example")
        self.setGeometry(100, 100, 600, 400)

        self.tree_table = TreeTable()

        # Set up the main layout
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.tree_table)

        self.setCentralWidget(central_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
