import sys
from PyQt5.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget

class TreeTableExample(QWidget):
    def __init__(self):
        super().__init__()

        # Create a QTreeWidget
        self.treeWidget = QTreeWidget()
        
        # Set column count for the tree widget
        self.treeWidget.setColumnCount(2)

        # Set header labels for the columns
        headers = {'Name': 0, 'Value': 1}
        self.treeWidget.setHeaderLabels(headers)

        # Create root item
        root_item = QTreeWidgetItem(self.treeWidget)
        root_item.setText(headers['Name'], 'Root')

        # Add child items
        child_item1 = QTreeWidgetItem(root_item)
        child_item1.setText(headers['Name'], 'Child 1')
        child_item1.setText(headers['Value'], 'Value 1')

        child_item2 = QTreeWidgetItem(root_item)
        child_item2.setText(headers['Name'], 'Child 2')
        child_item2.setText(headers['Value'], 'Value 2')

        # Set up layout
        layout = QVBoxLayout()
        layout.addWidget(self.treeWidget)
        self.setLayout(layout)

        # Set up main window
        self.setWindowTitle('TreeTable Example')
        self.setGeometry(100, 100, 400, 300)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TreeTableExample()
    window.show()
    sys.exit(app.exec_())
