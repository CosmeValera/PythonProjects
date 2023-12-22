from PyQt5.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
import sys

class TreeTable(QWidget):
    def __init__(self):
        super().__init__()

        self.tree = QTreeWidget()
        self.tree.setColumnCount(2)
        self.tree.setHeaderLabels(['ID', 'Name'])

        data = [
            ('1', 'Category 1', [('1.1', 'Item 1.1', [('1.1.1', 'Subitem 1.1.1')])]),
            ('2', 'Category 2', [('2.1', 'Item 2.1'), ('2.2', 'Item 2.2')]),
        ]
        self.addItemsRecursively(data)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tree)
        self.setLayout(self.layout)

    def addItemsRecursively(self, data, parentItem=None):
        for id_, name, items in data:
            item = QTreeWidgetItem(parentItem)
            item.setText(0, id_)
            item.setText(1, name)

            if items:
                self.addItemsRecursively(items, item)

            if parentItem is None:
                self.addTopLevelItem(item)
            else:
                parentItem.addChild(item)

app = QApplication(sys.argv)
window = TreeTable()
window.show()
sys.exit(app.exec_())
