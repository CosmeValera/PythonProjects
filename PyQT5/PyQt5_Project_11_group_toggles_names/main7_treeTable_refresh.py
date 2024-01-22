import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget

class TreeTable(QTreeWidget):
    def __init__(self, initial_expanded_values):
        super().__init__()

        data = [
            ('1', 'Category 1', [('1.1', 'Item 1.1', [('1.1.1', 'Subitem 1.1.1')])]),
            ('2', 'Category 2', [('2.1', 'Item 2.1'), ('2.2', 'Item 2.2')]),
        ]
        headers = ['Id', 'Name']

        self.setColumnCount(len(headers))
        self.setHeaderLabels(headers)
        
        # Connect the itemExpanded and itemCollapsed signals to the custom methods
        self.itemExpanded.connect(self.on_item_expanded)
        self.itemCollapsed.connect(self.on_item_collapsed)

        # Store the expanded items in a set
        self.expanded_items = set(initial_expanded_values)

        # Add items recursively, checking if they need to be expanded
        self.addItemsRecursively(self, data)

    def addItemsRecursively(self, parent, items):
        for item in items:
            currentItem = QTreeWidgetItem(parent, item[:2])
            if len(item) > 2:
                self.addItemsRecursively(currentItem, item[2])

            # Check if the current item's values are in the set of expanded values
            if tuple(item[:2]) in self.expanded_items:
                self.expandItem(currentItem)  # Expand the item

    def on_item_expanded(self, item):
        # Extract values from the expanded item
        values = [item.text(column) for column in range(self.columnCount())]

        # Store the expanded item in the set
        self.expanded_items.add(tuple(values))
        print("Expanded Item Values:", values, self.expanded_items)

    def on_item_collapsed(self, item):
        # Extract values from the collapsed item
        values = [item.text(column) for column in range(self.columnCount())]

        # Remove the item from the set when collapsed
        self.expanded_items.discard(tuple(values))
        print("Collapsed Item Values:", values, self.expanded_items)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle("With Refresh: TreeTable Example")
        self.setGeometry(100, 100, 600, 400)

        # Specify the initial expanded values
        initial_expanded_values = {('2', 'Category 2'), ('1.1', 'Item 1.1'), ('1', 'Category 1')}

        self.tree_table = TreeTable(initial_expanded_values)

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
