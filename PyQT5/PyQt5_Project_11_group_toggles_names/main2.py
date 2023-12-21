import sys
from PyQt5.QtWidgets import QApplication, QTreeView, QComboBox, QVBoxLayout, QWidget
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor


class GroupModel(QStandardItemModel):
    def __init__(self, original_data, parent=None):
        super(GroupModel, self).__init__(parent)
        self.original_data = original_data
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(["id", "number", "name"])
        for i in range(self.columnCount()):
            it = self.horizontalHeaderItem(i)
            it.setForeground(QColor("#191919"))

    def update_model(self, selected_header):
        self.clear()
        self.setHorizontalHeaderLabels(["id", "number", "name"])
        self.setColumnCount(3)
        for i in range(self.columnCount()):
            it = self.horizontalHeaderItem(i)
            it.setForeground(QColor("#565656"))

        categories = {}

        for row, item in enumerate(self.original_data):
            category_key = item[selected_header]
            if category_key not in categories:
                categories[category_key] = self.add_category(category_key)

            self.append_element_to_group(categories[category_key], item)

    def add_category(self, category_name):
        item_root = QStandardItem(category_name)
        item_root.setEditable(False)
        ii = self.invisibleRootItem()
        i = ii.rowCount()
        for j, it in enumerate((item_root,)):
            ii.setChild(i, j, it)
            ii.setEditable(False)
        for j in range(self.columnCount()):
            it = ii.child(i, j)
            if it is None:
                it = QStandardItem()
                ii.setChild(i, j, it)
            it.setBackground(QColor("#009842"))
            it.setForeground(QColor("#F2F2F2"))
        return item_root

    def append_element_to_group(self, group_item, item_data):
        j = group_item.rowCount()
        for i, text in enumerate(item_data.values()):
            item = QStandardItem(str(text))
            item.setEditable(False)
            item.setBackground(QColor("#0D1225"))
            item.setForeground(QColor("#F2F2F2"))
            group_item.setChild(j, i, item)

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.original_data = [
            {"id": "1", "number": "one", "name": "pepe"},
            {"id": "2", "number": "two", "name": "javi"},
            {"id": "3", "number": "one", "name": "javi"},
            {"id": "4", "number": "five", "name": "javi"},
            {"id": "1", "number": "four", "name": "marcos"}
        ]

        self.model = GroupModel(self.original_data, self)

        self.tree_view = QTreeView(self)
        self.tree_view.setModel(self.model)
        self.tree_view.setIndentation(0)
        self.tree_view.setExpandsOnDoubleClick(False)

        self.column_selector = QComboBox(self)
        self.column_selector.addItems(["", "id", "number", "name"])
        self.column_selector.currentIndexChanged.connect(self.group_by_column)

        layout = QVBoxLayout(self)
        layout.addWidget(self.column_selector)
        layout.addWidget(self.tree_view)

        self.setLayout(layout)

    def group_by_column(self, index):
        selected_header = self.column_selector.currentText()
        if selected_header:
            self.model.update_model(selected_header)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(720, 240)
    window.show()
    sys.exit(app.exec_())
