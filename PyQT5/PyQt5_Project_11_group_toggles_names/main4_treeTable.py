from PyQt5.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
import sys

class TreeTable(QWidget):
    def __init__(self):
        super().__init__()

        self.tree = QTreeWidget()
        self.tree.setColumnCount(2)
        self.tree.setHeaderLabels(['ID', 'Name'])

        data = [
            ('1', 'Category 1', [('1.1', 'Item 1.1'), ('1.2', 'Item 1.2')]),
            ('2', 'Category 2', [('2.1', 'Item 2.1'), ('2.2', 'Item 2.2')]),
        ]

        for id_, name, items in data:
            parent = QTreeWidgetItem(self.tree)
            parent.setText(0, id_)
            parent.setText(1, name)
            for id_, name in items:
                child = QTreeWidgetItem(parent)
                child.setText(0, id_)
                child.setText(1, name)
        
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tree)
        self.setLayout(self.layout)

app = QApplication(sys.argv)
window = TreeTable()
window.show()
sys.exit(app.exec_())
