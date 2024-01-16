from PyQt5.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class TreeWidgetDemo(QWidget):
    def __init__(self):
        super().__init__()

        self.tree = QTreeWidget(self)
        self.tree.setColumnCount(2)
        self.tree.setHeaderLabels(['🔍 Id', '🔍 Name'])

        data = [
            ('1', 'Category 1', [('1.1', 'Item 1.1')]),
            ('2', 'Category 2', [('2.1', 'Item 2.1'), ('2.2', 'Item 2.2')]),
        ]

        for id, name, children in data:
            parent = QTreeWidgetItem(self.tree)
            parent.setText(0, id)
            parent.setText(1, name)
            parent.setFlags(parent.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
            for child_id, child_name in children:
                child = QTreeWidgetItem(parent)
                child.setFlags(child.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
                child.setText(0, child_id)
                child.setText(1, child_name)

        layout = QVBoxLayout(self)
        layout.addWidget(self.tree)

if __name__ == '__main__':
    app = QApplication([])
    demo = TreeWidgetDemo()
    demo.show()
    app.exec_()
